from patchwork.lib.values import show_value
from patchwork.lib.values import value_type
from patchwork.exceptions import PatchworkInputError
from .mutated_dict import MutatedDict
from .mutated_list import MutatedList


def make_safe(container):
    if isinstance(container, MutatedDict) or isinstance(container, MutatedList):
        return container
    if isinstance(container, dict):
        return MutatedDict(container)
    if isinstance(container, list):
        return MutatedList(container)
    raise PatchworkInputError(
        f"Expected element of type list or dictionary, "
        f"found {show_value(container)} of type {value_type(container)}."
    )
