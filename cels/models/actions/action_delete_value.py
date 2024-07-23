from cels.lib.safe import safe_traverse
from cels.lib.safe import safe_del_value
from . import action


@action
def action_delete_value(
    output_dict, key, indices, change_value, patch, path, root_input_dict
):
    """Delete value from list."""

    # get container to modify
    container, index = safe_traverse(output_dict, key, indices)

    # delete element
    safe_del_value(container[index], change_value)
