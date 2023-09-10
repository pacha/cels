from patchwork.lib.value_type import value_type
from patchwork.exceptions import PatchworkInputError


def safe_get(container, index):
    """Get an element from a dictionary or list and raise PatchworkInputError in case of problem."""
    try:
        return container[index]
    except Exception as err:
        raise PatchworkInputError(
            f"Can't find element at '{index}' in container of type {value_type(container)}: {err}."
        )
