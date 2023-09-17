from cels.lib.show import show
from cels.exceptions import CelsInputError


def safe_get(container, index):
    """Get an element from a dictionary or list and raise CelsInputError in case of problem."""
    try:
        return container[index]
    except KeyError:
        raise CelsInputError(f"Cannot find key {show(index)}.")
    except IndexError:
        raise CelsInputError(f"Cannot find index {show(index)}.")
    except Exception:
        raise CelsInputError(f"Cannot find element at {show(index)}.")
