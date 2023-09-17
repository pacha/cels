from cels.lib.show import show_index
from cels.lib.show import show
from cels.exceptions import CelsInputError


def safe_del(container, index):
    """Delete an element from a container catching all possible exceptions."""
    try:
        del container[index]
    except Exception:
        raise CelsInputError(
            f"Cannot delete element with {show_index(index, container)} "
            f"from {show(container)}"
        )
