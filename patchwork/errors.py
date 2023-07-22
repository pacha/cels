from typing import Any

class PatchworkError(Exception):
    """Base exeption for PatchworkError errors."""

    pass


class PatchworkInternalError(Exception):
    """Error for unexpected states inside the application."""

    pass


class PatchworkInvalidPatch(Exception):
    """Invalid patch."""

    pass

class PatchworkInvalidChange(PatchworkInvalidPatch):
    """Invalid change in patch."""

    pass

class PatchworkInvalidOperation(PatchworkInvalidChange):
    """Invalid operation in patch."""

    pass

class PatchworkInvalidPosition(PatchworkInvalidChange):
    """Invalid position in patch."""

    pass

class PatchworkInvalidValue(PatchworkInvalidChange):
    """Invalid value in patch."""

    pass

class PatchworkInvalidValueType(PatchworkInvalidChange):
    """The patch operation is incompatible with the original or the patch value type"""
    def __init__(self, message: str, allowed_type: Any):
        super().__init__(message)
        self.allowed_type = allowed_type

