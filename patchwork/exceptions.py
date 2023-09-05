from typing import Any

class PatchworkException(Exception):
    """Patchwork base exeption."""

    pass

class PatchworkError(PatchworkException):
    """Base exeption for Patchwork errors."""

    pass

class PatchworkInputError(PatchworkError):
    """Invalid user provided data."""

    pass

class PatchworkInternalError(PatchworkError):
    """Exeption for internal, unexpected errors."""

    pass

class PatchworkActionException(PatchworkException):
    """Base exeption for Patchwork actions."""

    pass

class PatchworkActionPatch(PatchworkActionException):
    """Patch action exception."""
    def __init__(self, tail_container, tail_index, tail_path, input_dict, patch_dict):
        self.tail_container = tail_container
        self.tail_index = tail_index
        self.tail_path = tail_path
        self.input_dict = input_dict
        self.patch_dict = patch_dict

class PatchworkActionRename(PatchworkActionException):
    """Rename action exception."""

    pass

