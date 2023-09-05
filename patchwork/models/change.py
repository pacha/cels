from typing import Any
from dataclasses import field
from dataclasses import dataclass

from dacite import from_dict
from dacite import DaciteError
from typeguard import check_type
from typeguard import TypeCheckError

from .actions import actions
from .operation import Operation
from patchwork.lib.value_type import value_type
from patchwork.exceptions import PatchworkInputError

list_exclusive_operations = ["insert", "extend"]
operations_without_value = ["delete"]
allowed_operations_for_new_keys = ["set"]

list_operations = ["patch", "set", "delete", "insert", "extend"]
valid_operation_values = {
    "patch": dict,
    "set": Any,
    "delete": None,
    "rename": Any,
    "insert": Any,
    "extend": list,
    "var": Any,
    "link": str,
    "render": str,
}


@dataclass
class Change:
    operation: Operation | None
    value: Any
    indices: list[int | None] = field(default_factory=list)

    def __init__(
        self,
        operation: Operation | None,
        value: Any = None,
        indices: list[int | None] = [],
    ):
        if operation:
            # chech that the value type matches the allowed types
            try:
                check_type(value, operation.value_type)
            except TypeCheckError:
                raise PatchworkInputError(
                    f"Can't execute operation '{operation}' with the value found in "
                    f"the patch dictionary ('{value}'). "
                    f"This operation requires a patch value of type '{operation.value_type_name}' "
                    f"instead of type '{value_type(value)}'."
                )
            # check that the operation takes indices
            if not operation.takes_indices and indices:
                raise PatchworkInputError(
                    f"Operation '{operation}' can't take indices '{indices}'."
                )

        # set fields
        self.operation = operation
        self.value = value
        self.indices = indices

    @classmethod
    def from_dict(cls, data: dict):
        """Create instance from dictionary"""
        # get operation
        try:
            operation_name = data["operation"]
        except KeyError:
            raise PatchworkInputError(
                f"Missing 'operation' key in dictionary part of a 'change' list: {data}"
            )
        try:
            operation = Operation.get(operation_name)
        except KeyError:
            raise PatchworkInputError(
                f"The operation '{operation_name}' provided in the change list is not valid. "
                f"Valid operations are: {Operation.show_names()}."
            )

        # for some operations, it is fine to not to specify value
        value_missing = "value" not in data
        if value_missing:
            if operation.value_type is not None:
                raise PatchworkInputError(
                    f"Missing 'value' key in dictionary part of a 'change' list: {data}"
                )
            else:
                data["value"] = None

        # create change object
        try:
            data["operation"] = operation
            obj = from_dict(cls, data)
        except DaciteError as err:
            raise PatchworkInputError(err)
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

    def apply(self, output_dict, key, input_dict, patch, path):
        """Apply operation at key."""

        # find operation
        if self.operation:
            operation_name = self.operation.name
        else:
            try:
                input_value_is_dict = isinstance(output_dict[key], dict)
            except KeyError:
                input_value_is_dict = False
            patch_value_is_dict = isinstance(self.value, dict)
            operation_name = (
                "patch" if input_value_is_dict and patch_value_is_dict else "set"
            )

        # find action
        action = actions[operation_name]

        # apply action
        action(
            container=output_dict,
            key=key,
            indices=self.indices,
            change_value=self.value,
            input_dict=input_dict,
            patch=patch,
            path=path,
        )
