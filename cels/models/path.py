import re
from typing import Any
from typing import List
from dataclasses import dataclass

from cels.exceptions import CelsInputError

special_chars_pattern = re.compile(r"\.|\[|\]")


@dataclass
class Path:
    """Path to locate a value in a structure of nested dictionaries/lists.

    For example:

        .a.b[1].e

    Points to value '5' in this structure:

    {
        "a": {
            "b": [{"c": 3, "d": 4}, {"e": 5, "f": 6}]
            }
        }
    }

    The class is immutable and appending new parts, like in:

        path + "b"

    creates a new path object.

    Note: the . and [] notations are equivalent. For example,
    these two expressions describe the same path:

        .foo.bar[5].spam[eggs]
        .foo.bar.5.spam.eggs
    """

    expr: str

    def __init__(self, expr: str = ""):
        self.expr = expr

    def __str__(self):
        return self.expr if self.expr else "."

    def __add__(self, part: Any):
        """Create new path object by appending a new part."""
        # get separators
        if isinstance(part, int):
            left_separator, right_separator = "[", "]"
        else:
            left_separator, right_separator = ".", ""

        # get escape characters
        part_str = str(part) if part is not None else "_"
        if special_chars_pattern.search(part_str):
            left_escape, right_escape = '"', '"'
        else:
            left_escape, right_escape = "", ""

        # create new path
        new_expr = f"{self.expr}{left_separator}{left_escape}{part_str}{right_escape}{right_separator}"
        return Path(new_expr)

    def append(self, parts: List[Any]):
        new_path = self
        for part in parts:
            new_path = new_path + part
        return new_path

    def get_value(self, data: dict):
        """Get value for this path in the provided dictionary."""

        # get parts
        expr_pattern = r'\."([^"]+)"|\["([^"]+)"\]|\.([^.\[]+)|\[([^\]]+)\]'
        parts = [
            r.group(1) or r.group(2) or r.group(3) or r.group(4)
            for r in re.finditer(expr_pattern, self.expr)
        ]
        if not parts and self.expr not in ("", "."):
            raise CelsInputError(f'Impossible to parse path "{self.expr}"')

        # traverse data
        value = data
        for part in parts:
            try:
                index = int(part) if isinstance(value, list) else part
                value = value[index]
            except (KeyError, IndexError, TypeError):
                raise CelsInputError(
                    f'Impossible to find path element "{part}" while looking for "{self}"'
                )
        return value
