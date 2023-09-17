from patchwork.lib.values import show_value
from patchwork.exceptions import PatchworkInputError


def safe_get(container, index):
    """Get an element from a dictionary or list and raise PatchworkInputError in case of problem."""
    try:
        return container[index]
    except KeyError:
        raise PatchworkInputError(f"Cannot find key {show_value(index)}.")
    except IndexError:
        raise PatchworkInputError(f"Cannot find index {show_value(index)}.")
    except Exception:
        raise PatchworkInputError(f"Cannot find element at {show_value(index)}.")
