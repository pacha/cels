from patchwork.lib.values import show_value
from patchwork.lib.values import value_type
from patchwork.exceptions import PatchworkInputError


def safe_set(container, index, value):
    try:
        container[index] = value
    except Exception as err:
        raise PatchworkInputError(
            f"Can't set value {show_value(value)} at index {index} in container {show_value(container)}: {err}."
        )
