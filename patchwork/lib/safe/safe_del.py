
from patchwork.exceptions import PatchworkInputError

def safe_del(container, index):
    """Delete an element from a container catching all possible exceptions."""
    try:
        del container[index]
    except Exception as err:
        raise PatchworkInputError(
            f"Element at '{index}' can't be deleted: {err}."
        )
