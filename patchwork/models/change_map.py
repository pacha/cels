"""
A ChangeMap contains all the changes that need to be made to a dictionary
according to a Patch.

There's a different ChangeMap for each dictionary in a nested structure, and it
is always composed by two pieces of information:

* How items that already exists in the original dict should be changed (`changes`)
* What items should be added (`additions`)

The changes dictionary is created by translating the annotations of a Patch
dictionary into a normalized form. For example, the patch:

    {
        "foo": 1,
        "bar {rename}": "spam",
        "baz {delete}": None,
        "bat {change}": [
            {
                "operation": "rename",
                "value": "BAT",
            },
            {
                "operation": "extend",
                "value": [1, 2, 3],
                "position": 2,
            },
        },
    }

results in the following changes dict:

    {
        "foo": [Change(operation=Operation.set, value=1, position=None)],
        "bar": [Change(operation=Operation.rename, value="spam", position=None)],
        "bar": [Change(operation=Operation.delete, value=None, position=None)],
        "bat": [
            Change(operation=Operation.rename, value="BAT", position=None),
            Change(operation=Operation.append, value=[1, 2, 3], position=2),
        ],
    }

The `additions` dictionary is just a subset of the patch dictionary that
contains all the items with keys that are not present in the original dictionary.
None of those keys should be annotated, as annotations only make sense for
changes (for additions only 'patch' and 'set' operations are valid). Any key
that is annotated will result in an error. For example, this is invalid:

original_dict:

    {
        "a": 1,
    }

patch:

    {
        "b {rename}": "c",
    }

If none of the patch keys is present in the original dictionary, `additions` will
be exactly the same as the patch dictionary. Eg:

original_dict:

    {
        "a": 1,
    }

patch:

    {
        "foo": 2,
        "bar": {
            "baz": "spam",
        }
    }

additions:

    {
        "foo": 2,
        "bar": {
            "baz": "spam",
        }
    }

"""

from typing import Any
from typing import Optional
from dataclasses import dataclass

from dacite.exceptions import DaciteFieldError

from .change import Change
from .change import allowed_operations_for_new_keys
from .operation import Operation
from .annotation_config import AnnotationConfig
from patchwork.errors import PatchworkInvalidValue
from patchwork.errors import PatchworkInvalidPosition
from patchwork.errors import PatchworkInvalidOperation
from patchwork.errors import PatchworkInvalidValueType


@dataclass
class ChangeMap:
    parent: "ChangeMap"
    changes: dict[str, list["Change"]]
    additions: dict
    annotation_config: AnnotationConfig
    path: str
    level: int

    def __init__(
        self,
        original_dict: dict,
        patch: dict,
        parent: Optional["ChangeMap"] = None,
        annotation_config: AnnotationConfig = AnnotationConfig(),
    ):
        """Translate a patch into a change_map.

        A change_map can only be created if the original_dict is available
        since it is necessary to determine which keys are not in it in
        order to define the `new_data`.
        """
        # save parent
        self.parent = parent

        # save annotation configuration
        self.annotation_config = annotation_config

        # compute changes and additions
        self.changes = {}
        self.additions = {}
        for key, value in patch.items():
            # get annotation parts
            actual_key, operation_name, position = annotation_config.extract_annotation(
                key
            )

            # check if this item should go into new_data
            if actual_key not in original_dict:
                if (
                    operation_name is not None
                    and operation_name not in allowed_operations_for_new_keys
                ):
                    raise PatchworkInvalidOperation(
                        f"Invalid operation '{operation_name}' for key '{key}'. "
                        "(The only operations allowed for keys not present in the "
                        "original dictionary are {allowed_operations_for_new_keys})."
                    )
                patch_value = patch[key]
                if isinstance(patch_value, dict):
                    annotation_config.validate_no_annotations(patch_value)
                self.additions[actual_key] = patch_value
                continue

            # if no operation is provided, use "patch" or "set"
            if operation_name:
                operation = Operation(operation_name)
            else:
                patch_value_is_dict = isinstance(value, dict)
                original_dict_value_is_dict = isinstance(
                    original_dict[actual_key], dict
                )
                if patch_value_is_dict and original_dict_value_is_dict:
                    operation = Operation.patch
                else:
                    operation = Operation.set

            # get changes
            if operation == "change":
                change_value_is_list = isinstance(value, list)
                if not change_value_is_list:
                    raise PatchworkInvalidValue(
                        f"Invalid value '{value}' for key '{key}'. "
                        "(Change operations take a list of changes as value)."
                    )
                try:
                    changes = [Change.from_dict(change_data) for change_data in value]
                except DaciteFieldError as err:
                    raise PatchworkInvalidValue(
                        f"Invalid change for key '{key}'. "
                        "(Changes should be described with a dictionary "
                        'with structure {"operation": …, "value": …, "position": …}).\n'
                        f"Error: {err}."
                    )
            else:
                changes = [Change(operation=operation, value=value, position=position)]

            # check that changes are compatible with the original data they have
            # to be applied to.
            for change in changes:
                # check that the original value type matches the allowed types
                original_value = original_dict[actual_key]
                try:
                    change.operation.validate_against_original_value(original_value)
                except PatchworkInvalidValueType as err:
                    raise PatchworkInvalidOperation(
                        f"Can't execute operation '{operation.value}' with the value found in "
                        f"the original dictionary ('{original_value}'). "
                        f"This operation requires a value of type '{err.allowed_type}' instead of type "
                        f"'{type(original_value).__name__ if value is not None else 'None/null'}'."
                    )

                # check that the position is not out of bounds (if provided)
                if change.position is not None:
                    original_list = original_dict[actual_key]
                    original_list_length = len(original_list)
                    lower_bound = min([-original_list_length, -1])
                    upper_bound = max([original_list_length, 1])
                    if not (lower_bound <= change.position < upper_bound):
                        raise PatchworkInvalidPosition(
                            f"Position '{change.position}' for key '{key}' is out-of-bounds. "
                            f"The maximum index possible is '{upper_bound - 1}'."
                        )

                # check that in a set operation, the inner keys don't have annotations
                if change.operation == "set":
                    annotation_config.validate_no_annotations(change.value)

            # store changes
            self.changes[actual_key] = changes
