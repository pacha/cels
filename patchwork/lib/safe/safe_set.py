from patchwork.lib.values import show_value
from patchwork.lib.values import show_index
from patchwork.exceptions import PatchworkInputError


def safe_set(container, index, value):
    try:
        container[index] = value
    except Exception as err:
        raise PatchworkInputError(
            f"Cannot set value {show_value(value)} at {show_index(index, container)}: {err}"
        )
