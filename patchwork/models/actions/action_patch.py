from patchwork.lib.copy_on_write import safe_get
from patchwork.lib.copy_on_write import safe_traverse
from patchwork.exceptions import PatchworkInputError
from patchwork.exceptions import PatchworkActionPatch
from . import action


@action
def action_patch(output_dict, key, indices, change_value, input_dict, patch, path):
    """Patch value."""

    # get container to modify
    tail_container, tail_index = safe_traverse(output_dict, key, indices)
    tail_value = safe_get(tail_container, tail_index)
    if not isinstance(tail_value, dict):
        raise PatchworkInputError(
            "Can't patch a dictionary with anything other than another dictionary. "
            f"The provided patch value is of type '{type(tail_value)}'."
        )
    tail_path = (path + key).append(indices)

    raise PatchworkActionPatch(
        tail_container=tail_container,
        tail_index=tail_index,
        tail_path=tail_path,
        input_dict=tail_value,
        patch_dict=change_value,
    )
