from patchwork.lib.show import show_index
from patchwork.lib.show import show
from patchwork.exceptions import PatchworkInputError


def safe_del(container, index):
    """Delete an element from a container catching all possible exceptions."""
    try:
        del container[index]
    except Exception:
        raise PatchworkInputError(
            f"Cannot delete element with {show_index(index, container)} "
            f"from {show(container)}"
        )
