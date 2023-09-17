from patchwork.lib.values import show_index
from patchwork.lib.values import show_value
from patchwork.exceptions import PatchworkInputError


def safe_del(container, index):
    """Delete an element from a container catching all possible exceptions."""
    try:
        del container[index]
    except Exception:
        raise PatchworkInputError(
            f"Cannot delete element with {show_index(index, container)} "
            f"from {show_value(container)}"
        )
