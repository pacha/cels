from patchwork.lib.safe import safe_get
from patchwork.lib.safe import safe_traverse
from patchwork.lib.values import value_type
from patchwork.exceptions import PatchworkInputError
from patchwork.exceptions import PatchworkActionPatch
from . import action


@action
def action_patch(output_dict, key, indices, change_value, patch, path, root_input_dict):
    """Patch value."""

    # get container to modify
    tail_container, tail_index = safe_traverse(output_dict, key, indices)
    try:
        tail_value = tail_container[tail_index]
        if not isinstance(tail_value, dict):
            raise ValueError
    except Exception:
        tail_value = {}
        tail_container[tail_index] = tail_value

    tail_path = (path + key).append(indices)

    raise PatchworkActionPatch(
        tail_container=tail_container,
        tail_index=tail_index,
        tail_path=tail_path,
        input_dict=tail_value,
        patch_dict=change_value,
    )
