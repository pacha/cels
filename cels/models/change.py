from typing import Any
from typing import List
from typing import Union
from dataclasses import field
from dataclasses import dataclass

from typeguard import check_type
from typeguard import TypeCheckError

from .actions import actions
from .operation import Operation
from cels.lib.show import show
from cels.lib.show import show_type
from cels.exceptions import CelsInputError


@dataclass
class Change:
    operation: Union[Operation, None]
    value: Any
    indices: List[Union[int, None]] = field(default_factory=list)

    def __init__(
        self,
        operation: Union[Operation, None],
        value: Any = None,
        indices: List[Union[int, None]] = [],
    ):
        if operation:
            # chech that the value type matches the allowed types
            try:
                check_type(value, operation.value_type)
            except TypeCheckError:
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
        """Apply operation at key."""

        # find operation
        if self.operation:
            operation_name = self.operation.name
        else:
            patch_value_is_dict = isinstance(self.value, dict)
            operation_name = "patch" if patch_value_is_dict else "set"

        # find action
        action = actions[operation_name]

        # apply action
        action(
            container=output_dict,
            key=key,
            indices=self.indices,
            change_value=self.value,
            patch=patch,
            path=path,
            root_input_dict=root_input_dict,
        )
