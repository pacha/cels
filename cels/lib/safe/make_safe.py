from cels.lib.show import show
from cels.lib.show import show_type
from cels.exceptions import CelsInputError
from .mutated_dict import MutatedDict
from .mutated_list import MutatedList

# Pre-built type dispatch table for fast type resolution in make_safe.
# Using type(container) as a dict key is faster than chained isinstance()
# checks, especially since MutatedDict/MutatedList are common in hot paths
# after the first traversal.
_dict_type = type({})   # builtins.dict
_list_type = type([])   # builtins.list
_md_type = MutatedDict
_ml_type = MutatedList

_make_safe_dispatch = {
    _md_type: lambda c: c,
    _ml_type: lambda c: c,
    _dict_type: MutatedDict,
    _list_type: MutatedList,
}


def make_safe(container):
    """Make a container safe to modify by wrapping in MutatedDict/MutatedList."""
    dispatch = _make_safe_dispatch.get(type(container))
    if dispatch is not None:
        return dispatch(container)
    raise CelsInputError(
        f"Expected element of type list or dictionary, "
        f"found value {show(container)} of type {show_type(container)}."
    )
