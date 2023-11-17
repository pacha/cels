from typing import Any
from typing import List
from typing import Dict
from typing import Union
from typing import ClassVar
from dataclasses import dataclass

from cels.exceptions import CelsInternalError

# unfortunately we can't pass forward-references to check_type.
# we'll use this map to get the actual type hints.
hints_map = {
    "Any": Any,
    "str": str,
    "dict": dict,
    "list": list,
    "None": None,
    "list[dict[str, Any]]": List[Dict[str, Any]],
    "str | int | bool | None": Union[str, int, bool, None],
}


@dataclass
class Operation:
    # class attributes
    instances: ClassVar[Dict[str, "Operation"]] = {}

    # instance attributes
    name: str
    format: str
    description: str
    notes: str
    examples: List[Dict[str, str]]
    takes_indices: bool
    takes_underscore_index: bool
    requires_value: bool
    value_type: Any

    @classmethod
    def add(
        cls,
        name: str,
        format: str,
        description: str,
        notes: str,
        examples: list,
        takes_indices: bool,
        takes_underscore_index: bool,
        requires_value: bool,
        value_type: str,
    ) -> "Operation":
        if not takes_indices and takes_underscore_index:
            raise CelsInternalError(
                "Operations can have 'takes_underscore_index' set to true if 'takes_indices' is set to false"
            )
        instance = cls(
            name,
            format,
            description,
            notes,
            examples,
            takes_indices,
            takes_underscore_index,
            requires_value,
            hints_map[value_type],
        )
        cls.instances[name] = instance
        return instance

    @classmethod
    def get(cls, name: str) -> "Operation":
        return cls.instances[name]

    @classmethod
    def get_all(cls) -> "List[Operation]":
        return list(cls.instances.values())

    def __str__(self):
        return self.name

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Operation):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        return False
