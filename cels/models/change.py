from typing import Any
from typing import List
from typing import Union
from dataclasses import field
from dataclasses import dataclass

from .actions import actions
from .operation import Operation
from cels.lib.show import show
from cels.lib.show import show_type
from cels.exceptions import CelsInputError


def _check_value_type(value, value_type) -> bool:
    """Lightweight type check replacing typeguard.check_type.

    Returns True if value matches the expected type, False otherwise.
    This avoids the significant overhead of typeguard's runtime introspection.
    """
    # Any type always passes
    if value_type is Any:
        return True

    # Simple types
    if value_type is str:
        return isinstance(value, str)
    if value_type is dict:
        return isinstance(value, dict)
    if value_type is list:
        return isinstance(value, list)

    # Union types (e.g., Union[str, int, bool, None])
    origin = getattr(value_type, "__origin__", None)
    if origin is Union:
        args = value_type.__args__
        for arg in args:
            if arg is type(None):
                if value is None:
                    return True
            elif isinstance(value, arg):
                return True
        return False

    # Generic list types (e.g., List[Dict[str, Any]])
    if origin is list:
        if not isinstance(value, list):
            return False
        # Check element types for List[Dict[str, Any]]
        args = getattr(value_type, "__args__", ())
        if args and value:
            elem_type = args[0]
            elem_origin = getattr(elem_type, "__origin__", None)
            if elem_origin is dict:
                return all(isinstance(item, dict) for item in value)
        return True

    # Fallback: use isinstance for other types
    try:
        return isinstance(value, value_type)
    except TypeError:
        return True


@dataclass
class Change:
    operation: Union[Operation, None]
    value: Any
    indices: List[Union[int, None]] = field(default_factory=list)

    def __init__(
        self,
        operation: Union[Operation, None],
        value: Any = None,
        indices: Union[List[Union[int, None]], None] = None,
    ):
        # Fix mutable default argument: use None and create a new list per instance.
        # The previous `indices=[]` was a classic Python gotcha where the same list
        # object was shared across all Change instances that used the default.
        if indices is None:
            indices = []

        if operation:
            # check that the value type matches the allowed types
            if not _check_value_type(value, operation.value_type):
                raise CelsInputError(
                    f"Cannot execute operation {show(operation)} with value {show(value)}. "
                    f"This operation requires a value of type {show_type(operation.value_type)}"
                )
            # check that the operation takes indices
            if not operation.takes_indices and indices:
                raise CelsInputError(
                    f"Operation {show(operation)} cannot take indices (provided {show(indices)})"
                )

        # set fields
        self.operation = operation
        self.value = value
        self.indices = indices

        # Pre-resolve the action function to avoid dict lookup at apply time
        if operation:
            self._action = actions.get(operation.name)
        else:
            self._action = None

    @classmethod
    def from_dict(cls, data: dict):
        """Create instance from dictionary"""
        # get operation
        try:
            operation_name = data["operation"]
        except KeyError:
            raise CelsInputError(f"Missing 'operation' key in {show(data)}")
        try:
            operation = Operation.get(operation_name)
        except KeyError:
            raise CelsInputError(
                f"Wrong operation: {show(operation_name)} in change list"
            )

        # for some operations, it is fine to not to specify value
        try:
            value = data["value"]
        except KeyError:
            if operation.requires_value:
                raise CelsInputError(f"Missing 'value' key in {show(data)}")
            else:
                value = None

        # indices must me a list of integers
        indices = data.get("indices", [])
        if not isinstance(indices, list):
            raise CelsInputError(
                f"'indices' field must be of type list instead of {show_type(indices)}"
            )
        for index in indices:
            if not isinstance(index, int) or index == "_":
                raise CelsInputError("'indices' field must be a list of integers")

        # check no extra fields
        extra_fields = set(data.keys()) - {"operation", "value", "indices"}
        if extra_fields:
            raise CelsInputError(
                f"Found invalid keys in change dictionary: {show(extra_fields)}"
            )

        # create change object
        obj = cls(
            operation=operation,
            value=value,
            indices=indices,
        )
        return obj

    def __str__(self):
        if not self.operation:
            return ""
        index_str = (
            ("@" + ",".join([str(index) for index in self.indices]))
            if self.indices
            else ""
        )
        return f"{{{self.operation.name}{index_str}}}"

    def apply(self, output_dict, key, patch, path, root_input_dict):
        """Apply operation at key and return any action signal."""

        # Use pre-resolved action if available, otherwise resolve now
        action = self._action
        if action is None:
            # Determine operation name for unannotated keys
            if self.operation:
                action = actions[self.operation.name]
            else:
                patch_value_is_dict = isinstance(self.value, dict)
                operation_name = "patch" if patch_value_is_dict else "set"
                action = actions[operation_name]

        # apply action and return result (may be a signal object like CelsActionPatch)
        return action(
            container=output_dict,
            key=key,
            indices=self.indices,
            change_value=self.value,
            patch=patch,
            path=path,
            root_input_dict=root_input_dict,
        )
