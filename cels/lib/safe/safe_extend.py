from cels.lib.show import show_index
from cels.lib.show import show
from cels.exceptions import CelsInputError


def safe_extend(container, index, value):
    if not isinstance(container, list):
        raise CelsInputError(
            f"Cannot perform operation at {show_index(index, container)}: "
            f"value {show(container)} is not a list."
        )
    if not isinstance(value, list):
        raise CelsInputError(
            f"Cannot perform operation at {show_index(index, container)}: "
            f"value {show(value)} is not a list."
        )
    if index is None:
        container.extend(value)
    else:
        if not isinstance(index, int):
            raise CelsInputError(
                f"Cannot perform operation at {show_index(index, container)}: "
                "index must be an integer."
            )
        length = len(container)
        lower_boundary, upper_boundary = -length, max(length, 1)
        if not (lower_boundary <= index < upper_boundary):
            raise CelsInputError(
                f"List index {show(index)} out of range [{lower_boundary}, {upper_boundary - 1}]."
            )
        container[index:index] = value
