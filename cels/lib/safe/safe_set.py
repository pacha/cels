from cels.lib.show import show
from cels.lib.show import show_index
from cels.exceptions import CelsInputError


def safe_set(container, index, value):
    try:
        container[index] = value
    except Exception as err:
        raise CelsInputError(
            f"Cannot set value {show(value)} at {show_index(index, container)}: {err}"
        )
