from patchwork.lib.value_type import value_type
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
        f"Object of type {value_type(container)} is not a list or a dictionary"
    )
