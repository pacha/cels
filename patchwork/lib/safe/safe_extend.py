from patchwork.lib.values import value_type
from patchwork.exceptions import PatchworkInputError


def safe_extend(container, index, value):
    if not isinstance(container, list):
        raise PatchworkInputError(
            f"Can't perform operation at '{index}': receiving container of type "
            f"'{value_type(container)} is not a list."
        )
    if not isinstance(value, list):
        raise PatchworkInputError(
            f"Can't extend list at '{index}': value of type "
            f"'{value_type(value)} is not a list."
        )
    if index is None:
        container.extend(value)
    else:
        if not isinstance(index, int):
            raise PatchworkInputError(
                f"Can't use index '{index}': operating on a list requires an index "
                f"of type integer (not '{value_type(index)}')."
            )
        length = len(container)
        lower_boundary, upper_boundary = -length, max(length, 1)
        if not (lower_boundary <= index < upper_boundary):
            raise PatchworkInputError(
                f"List index '{index}' out of range ({lower_boundary}, {upper_boundary})."
            )
        container[index:index] = value
