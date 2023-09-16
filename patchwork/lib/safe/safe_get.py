from patchwork.exceptions import PatchworkInputError


def safe_get(container, index):
    """Get an element from a dictionary or list and raise PatchworkInputError in case of problem."""
    try:
        return container[index]
    except KeyError:
        raise PatchworkInputError(f"Can't find key {index}.")
    except IndexError:
        raise PatchworkInputError(f"Can't find index {index}.")
    except Exception:
        raise PatchworkInputError(f"Can't find element at {index}.")
