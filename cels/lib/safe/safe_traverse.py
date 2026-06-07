from .safe_get import safe_get
from .make_safe import make_safe
from cels.lib.show import show
from cels.exceptions import CelsInputError


def safe_traverse(container, key, indices):
    """Traverse a chain of nested lists making them safe to modify.

    Uses an iterative loop instead of recursion to avoid O(n²) list slicing
    (indices[1:] creates a new list on each recursion step) and to prevent
    stack overflow for deeply nested index chains.
    """
    if not indices:
        return container, key

    # Iterate through the index chain without creating intermediate lists
    current_container = container
    current_key = key
    for i, index in enumerate(indices):
        next_container = safe_get(current_container, current_key)
        if not isinstance(next_container, list):
            index_str = show(index) if index else "_"
            raise CelsInputError(f"Cannot use index {index_str} on a non-list value")
        safe_container = make_safe(next_container)
        current_container[current_key] = safe_container
        current_container = safe_container
        current_key = index

    return current_container, current_key
