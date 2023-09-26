from cels.lib.show import show
from cels.lib.show import show_type
from cels.exceptions import CelsInputError
from .mutated_dict import MutatedDict
from .mutated_list import MutatedList


def make_safe(container):
    if isinstance(container, MutatedDict) or isinstance(container, MutatedList):
        return container
    if isinstance(container, dict):
        return MutatedDict(container)
    if isinstance(container, list):
        return MutatedList(container)
    raise CelsInputError(
        f"Expected element of type list or dictionary, "
        f"found value {show(container)} of type {show_type(container)}."
    )
