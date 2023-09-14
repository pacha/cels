from patchwork.exceptions import PatchworkInputError
from patchwork.exceptions import PatchworkActionRename
from . import action


@action
def action_rename(
    output_dict, key, indices, change_value, patch, path, root_input_dict
):
    """Raise exception to notify a key rename."""

    # check that key is present
    if key not in output_dict:
        raise PatchworkInputError(
            f"Can't rename key '{key}' by '{change_value}': key '{key}' not present."
        )

    # signal the calling code to rename the key
    raise PatchworkActionRename
