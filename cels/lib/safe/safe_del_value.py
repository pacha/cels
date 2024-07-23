from cels.lib.show import show
from cels.exceptions import CelsInputError


def safe_del_value(container, value):
    if not isinstance(container, list):
        raise CelsInputError(
            f"Cannot perform operation: value {show(container)} is not a list."
        )
    container[:] = [element for element in container if element != value]
