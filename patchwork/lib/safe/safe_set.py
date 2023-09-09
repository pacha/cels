
from patchwork.lib.value_type import value_type
from patchwork.exceptions import PatchworkInputError

def safe_set(container, index, value):
    try:
        container[index] = value
    except Exception as err:
        raise PatchworkInputError(
            f"Can't set value at '{index}' in container of type {value_type(container)}: {err}."
        )
