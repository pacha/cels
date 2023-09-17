from patchwork.lib.safe import safe_set
from patchwork.lib.safe import safe_traverse
from patchwork.lib.show import show
from patchwork.exceptions import PatchworkInputError
from . import action


@action
def action_use(output_dict, key, indices, change_value, patch, path, root_input_dict):
    """Use a patch variable to set the value."""

    # get container to modify
    container, index = safe_traverse(output_dict, key, indices)

    # get value
    try:
        var_value = patch.get_var(change_value)
    except KeyError:
        raise PatchworkInputError(f"Variable {show(change_value)} not defined.")

    # perform action
    safe_set(container, index, var_value)
