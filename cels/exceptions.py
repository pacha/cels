from typing import Any


class CelsException(Exception):
    """Cels base exeption."""

    pass


class CelsError(CelsException):
    """Base exeption for Cels errors."""

    pass


class CelsInputError(CelsError):
    """Invalid user provided data."""

    pass


class CelsInternalError(CelsError):
    """Exeption for internal, unexpected errors."""

    pass


class CelsActionException(CelsException):
    """Base exeption for Cels actions."""

    pass


class CelsActionPatch(CelsActionException):
    """Patch action exception.

    Note: Also used as a signal object (not raised) for performance.
    When used as a signal, it is returned from action_patch instead of raised.
    """

    def __init__(self, tail_container, tail_index, tail_path, input_dict, patch_dict):
        self.tail_container = tail_container
        self.tail_index = tail_index
        self.tail_path = tail_path
        self.input_dict = input_dict
        self.patch_dict = patch_dict


class CelsActionRename(CelsActionException):
    """Rename action exception.

    Note: Also used as a signal (not raised) for performance.
    When used as a signal, it is returned from action_rename instead of raised.
    """

    pass
