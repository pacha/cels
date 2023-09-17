from cels.lib.safe import safe_traverse
from cels.lib.safe import safe_set
from . import action


@action
def action_set(output_dict, key, indices, change_value, patch, path, root_input_dict):
    """Set new value."""

    container, index = safe_traverse(output_dict, key, indices)
    patch.annotation_config.check_no_annotations(change_value)
    safe_set(container, index, change_value)
