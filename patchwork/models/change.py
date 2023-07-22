from typing import Any
from textwrap import shorten
from dataclasses import dataclass

from dacite import from_dict
from dacite import Config

from .operation import Operation
from patchwork.errors import PatchworkInvalidPosition
from patchwork.errors import PatchworkInvalidOperation
from patchwork.errors import PatchworkInvalidValueType
from patchwork.errors import PatchworkInternalError

list_operations = ["patch", "set", "delete", "insert", "extend"]
list_exclusive_operations = ["insert", "extend"]
operations_without_value = ["delete"]
allowed_operations_for_new_keys = ["set"]

@dataclass
class Change:
    operation: Operation
    value: Any
    position: int | None = None

    def __init__(self, operation: Operation, value: Any, position: int | None = None):
        # chech that the value type matches the allowed types
        try:
            operation.validate_against_patch_value(value)
        except PatchworkInvalidValueType as err:
            raise PatchworkInvalidOperation(
                f"Can't execute operation '{operation.value}' with the value found in "
                f"the patch dictionary ('{value}'). "
                f"This operation requires a patch value of type '{err.allowed_type}' "
                f"instead of type '{type(value).__name__ if value is not None else 'None/null'}'."
            )

        # check that 'position' is only provided for list operations
        if not isinstance(position, type(None)):
            if isinstance(position, int):
                if operation.value not in list_operations:
                    raise PatchworkInvalidPosition(
                        f"Position field {position} can't be used for operation {operation}. "
                        f"It is only allowed for operations {list_operations}."
                    )
        # set fields
        self.operation = operation
        self.value = value
        self.position = position

    @classmethod
    def from_dict(cls, data: dict):
        """Create instance from dictionary"""

        # for some operations, it is fine to not to specify value
        value_can_be_missing = "operation" in data and data["operation"] in operations_without_value
        value_missing = "value" not in data
        if value_can_be_missing and value_missing:
            data["value"] = None

        return from_dict(cls, data, config=Config(cast=[Operation]))

    def get_suffix(self):
        if self.position:
            return f"[{self.position}]"
        elif self.operation.value in list_exclusive_operations:
            return "[]"
        else:
            return ""

    def __str__(self):
        return f"{self.operation.value} | value: {shorten(str(self.value), width=40, placeholder=' ...')}"
