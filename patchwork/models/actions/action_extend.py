from patchwork.lib.safe import safe_traverse
from patchwork.lib.safe import safe_extend
from . import action


@action
def action_extend(
    output_dict, key, indices, change_value, patch, path, root_input_dict
):
    """Extend a list with another list."""

    container, index = safe_traverse(output_dict, key, indices)
    if not indices:
        safe_extend(container[index], None, change_value)
    else:
        safe_extend(container, index, change_value)
