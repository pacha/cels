from patchwork.lib.show import show
from patchwork.lib.show import show_index
from patchwork.exceptions import PatchworkInputError


def safe_set(container, index, value):
    try:
        container[index] = value
    except Exception as err:
        raise PatchworkInputError(
            f"Cannot set value {show(value)} at {show_index(index, container)}: {err}"
        )
