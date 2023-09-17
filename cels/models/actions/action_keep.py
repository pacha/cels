from cels.lib.safe import safe_traverse
from cels.lib.safe import safe_get
from . import action


@action
def action_keep(output_dict, key, indices, change_value, patch, path, root_input_dict):
    """Keep current value."""

    # 'keep' is a noop action, so we only check the validity of the index
    container, index = safe_traverse(output_dict, key, indices)
    _ = safe_get(container, index)
