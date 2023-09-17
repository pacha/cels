from cels.models import Path
from cels.lib.safe import safe_traverse
from cels.lib.safe import safe_set
from . import action


@action
def action_link(output_dict, key, indices, change_value, patch, path, root_input_dict):
    """Set the value pointed by a path in root_input_dict as new value."""

    # get container to modify
    container, index = safe_traverse(output_dict, key, indices)

    # get value
    input_path = Path(change_value)
    linked_value = input_path.get_value(root_input_dict)

    # perform action
    safe_set(container, index, linked_value)
