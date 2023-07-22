import logging as log
from enum import Enum
from typing import Any

from typeguard import check_type
from typeguard import TypeCheckError

from patchwork.errors import PatchworkInternalError
from patchwork.errors import PatchworkInvalidValueType

allowed_patch_value_types = {
    "change": list,
    "patch": dict,
    "set": Any,
    "delete": None,
    "rename": Any,
    "insert": Any,
    "extend": list,
}

allowed_original_value_types = {
    "change": Any,
    "patch": dict,
    "set": Any,
    "delete": Any,
    "rename": Any,
    "insert": list,
    "extend": list,
}

type_names = {
    str: "string (str)",
    dict: "dictionary (dict)",
    list: "list",
    None: "None/null",
    Any: "any",
}


class Operation(str, Enum):
    change = "change"
    patch = "patch"
    set = "set"
    rename = "rename"
    delete = "delete"
    insert = "insert"
    extend = "extend"

    @classmethod
    def list(cls):
        return [element.value for element in cls]

    def validate_against_patch_value(self, value: Any) -> bool:
        return self.validate_against_value(value, allowed_patch_value_types)

    def validate_against_original_value(self, value: Any) -> bool:
        return self.validate_against_value(value, allowed_original_value_types)

    def validate_against_value(self, value: Any, type_map: dict[str, Any]):
        allowed_type = type_map[self.value]
        try:
            check_type(value, allowed_type)
        except TypeCheckError:
            raise PatchworkInvalidValueType(
                message=f"The type of value '{value}' for operation '{self.value}' is invalid.",
                allowed_type=type_names[allowed_type],
            )

    def execute(self, key: Any, value: Any, change: "Change", result: dict) -> Any:
        try:
            operation_method = getattr(self, f"execute_{self.value}")
        except AttributeError:
            raise PatchworkInternalError(f"Operation {self.value} not implemented")
        return operation_method(key, value, change, result)

    def execute_set(self, key: Any, value: Any, change: "Change", result: dict) -> Any:
        """Set the original item with the provided change."""
        result[key] = change.value
        return key

    def execute_rename(
        self, key: Any, value: Any, change: "Change", result: dict
    ) -> Any:
        old_key = key
        new_key = change.value
        if old_key in result:
            result[new_key] = result[old_key]
            del result[old_key]
        else:
            result[new_key] = value
        return new_key

    def execute_delete(
        self, key: Any, value: Any, change: "Change", result: dict
    ) -> Any:
        if change.position is not None:
            if key not in result:
                result[key] = value[:]
            try:
                del result[key][change.position]
            except KeyError:
                pass
        else:
            try:
                del result[key]
            except KeyError:
                pass
        return key

    def execute_insert(
        self, key: Any, value: Any, change: "Change", result: dict
    ) -> Any:
        if change.position is None:
            result[key] = value[:] + [change.value]
        else:
            result[key] = value[:]
            result[key].insert(change.position, change.value)
        return key

    def execute_extend(
        self, key: Any, value: Any, change: "Change", result: dict
    ) -> Any:
        if change.position is None:
            result[key] = value[:] + change.value
        else:
            result[key] = value[:]
            result[key][change.position : change.position] = change.value

