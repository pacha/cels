from patchwork.lib.show import show
from patchwork.exceptions import PatchworkInputError


def safe_get(container, index):
    """Get an element from a dictionary or list and raise PatchworkInputError in case of problem."""
    try:
        return container[index]
    except KeyError:
        raise PatchworkInputError(f"Cannot find key {show(index)}.")
    except IndexError:
        raise PatchworkInputError(f"Cannot find index {show(index)}.")
    except Exception:
        raise PatchworkInputError(f"Cannot find element at {show(index)}.")
