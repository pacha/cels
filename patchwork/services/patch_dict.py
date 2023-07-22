import logging as log
from copy import deepcopy

from patchwork.models import ChangeMap
from patchwork.models import AnnotationConfig
from patchwork.errors import PatchworkInvalidPatch
from patchwork.errors import PatchworkInvalidChange


def patch_dict(
    original_dict: dict,
    patch: dict,
    separator: str = " ",
    left_marker: str = "{",
    right_marker: str = "}",
    do_deepcopy: bool = False,
) -> dict:
    """Patch a dictionary."""
    # get annotation config
    annotation_config = AnnotationConfig(separator, left_marker, right_marker)
    log.info(f"Annotation regex: {annotation_config.annotation_regex.pattern}")

    # get patch original dict
    result = patch_dict_rec(
        path="",
        original_dict=original_dict,
        patch=patch,
        parent_change_map=None,
        annotation_config=annotation_config
    )
    return deepcopy(result) if do_deepcopy else result


def patch_dict_rec(
    path: str,
    original_dict: dict,
    patch: dict,
    parent_change_map: ChangeMap | None,
    annotation_config: AnnotationConfig
) -> dict:
    """Recursive function to patch each level of the original dictionary using patch."""

    try:
        # convert the patch file in lists of Changes
        change_map = ChangeMap(original_dict, patch, parent_change_map, annotation_config)

        # patch all keys present in the original dict
        result = {}
        for original_key, original_value in original_dict.items():
            if original_key not in change_map.changes:
                new_path = f"{path}.{original_key}"
                log.info(f"{new_path} (unmodified)")
                result[original_key] = original_value
            else:
                changes = change_map.changes[original_key]
                result_key = original_key
                for change in changes:
                    new_path = f"{path}.{original_key}{change.get_suffix()}"
                    log.info(f"{new_path} ({change})")
                    if change.operation.value == "patch":
                        result[result_key] = patch_dict_rec(
                            path=f"{new_path}",
                            original_dict=original_value,
                            patch=change.value,
                            parent_change_map=change_map,
                            annotation_config=annotation_config
                        )
                    else:
                        result_key = change.operation.execute(
                            key=result_key,
                            value=original_value,
                            change=change,
                            result=result
                        )
    except PatchworkInvalidChange as err:
        path_str = path or ". (root)"
        raise PatchworkInvalidPatch(f"Error found at {path_str}: {err}")

    # add all keys only present in the patch
    for patch_key, patch_value in change_map.additions.items():
        log.info(f"{path}.{patch_key} (set)")
        result[patch_key] = patch_value

    return result

