from cels.lib.safe import safe_traverse
from cels.lib.safe import safe_del
from . import action


@action
def action_delete(
    output_dict, key, indices, change_value, patch, path, root_input_dict
):
    """Delete an element."""

    # get container to modify
    container, index = safe_traverse(output_dict, key, indices)

    # delete element
    safe_del(container, index)
