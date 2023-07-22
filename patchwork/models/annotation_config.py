import re
from typing import Any
from typing import Tuple
from dataclasses import dataclass

from .operation import Operation
from patchwork.errors import PatchworkInvalidPosition
from patchwork.errors import PatchworkInvalidOperation


@dataclass
class AnnotationConfig:
    separator: str
    left_marker: str
    right_marker: str
    annotation_regex: re.Pattern
    operation_regex: re.Pattern

    def __init__(
        self, separator: str = " ", left_marker: str = "{", right_marker: str = "}"
    ):
        # components
        self.separator = re.escape(separator)
        self.left_marker = re.escape(left_marker)
        self.right_marker = re.escape(right_marker)

        # annotation regex
        annotation_pattern = f"^(.+){ separator }{ left_marker }(.+){ right_marker }$"
        self.annotation_regex = re.compile(annotation_pattern)

        # operation regex
        operation_pattern = r"^([a-z]+)(@(-?[0-9]+))?$"
        self.operation_regex = re.compile(operation_pattern)

    def extract_annotation(
        self, annotated_key: str
    ) -> Tuple[Any, str | None, int | None]:
        """Extract the parts of an annotated key.

        Examples:
            * foo -> ("foo", None, None)
            * foo {operation} -> ("foo", "operation", None)
            * foo {operation@position} -> ("foo", "operation", "position")
        """
        # check if the key is not a string
        if not isinstance(annotated_key, str):
            return (annotated_key, None, None)

        # check if the key is not annotated
        annotation_data = self.annotation_regex.match(annotated_key)
        if not annotation_data:
            return (annotated_key, None, None)

        # extract annotation from key
        original_key = annotation_data.group(1)
        operation_string = annotation_data.group(2)

        # extract operation from annotation
        operation_data = self.operation_regex.match(operation_string)
        valid_operations = Operation.list()
        if not operation_data:
            raise PatchworkInvalidOperation(
                f"Invalid operation '{operation_string}' for key '{original_key}'. "
                f"Valid operations are: {valid_operations}. "
                "For operations such as 'insert' and 'extend', a position can also "
                "be provided after an @ sign. Eg. insert@2."
            )
        operation_name = operation_data.group(1)
        if operation_name not in valid_operations:
            raise PatchworkInvalidOperation(
                f"Invalid operation '{operation_name}' for key '{original_key}'. "
                f"Valid operations are: {valid_operations}. "
            )

        operation_position = operation_data.group(3)
        if operation_position is not None:
            try:
                operation_position = int(operation_position)
            except (ValueError, TypeError):
                raise PatchworkInvalidPosition(
                    f"Position '{operation_position}' for operation '{operation_name}' "
                    f"in key '{annotated_key} is invalid. Position must be an integer "
                    "(negative values are valid)."
                )

        return (original_key, operation_name, operation_position)

    def validate_no_annotations(self, data: Any) -> None:
        """Check recursively that there are no annotations in the provided dictionary."""
        # annotations can only appear in keys of dictionaries
        if not isinstance(data, dict):
            return

        # check each key and follow the values recursively
        for key, value in data.items():
            if isinstance(key, str):
                annotation = self.annotation_regex.match(key)
                if annotation:
                    raise PatchworkInvalidOperation(
                        f"Invalid child annotated key '{key}' in the patch. "
                        "Child keys can't be annotated neither after a 'set' operation nor "
                        "when the key doesn't appear in the original dictionary for other operations."
                    )
            self.validate_no_annotations(value)
