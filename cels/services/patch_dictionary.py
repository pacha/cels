from typing import Optional
import logging

from cels import default
from cels.logs import log
from cels.models import Path
from cels.models import Patch
from cels.models import KeyLocation
from cels.models import AnnotationConfig
from cels.exceptions import CelsInputError
from cels.exceptions import CelsActionPatch
from cels.exceptions import CelsActionRename

# Check logging level once to avoid per-call overhead in hot loop
_log_info_enabled = log.isEnabledFor(logging.INFO)

# Cache the type for fast isinstance checks in the hot loop
_CelsActionPatch = CelsActionPatch
_CelsActionRename = CelsActionRename


def patch_dictionary(
    input_dict: dict,
    patch_dict: dict,
    separator: str = default.separator,
    left_marker: str = default.left_marker,
    index_marker: str = default.index_marker,
    right_marker: str = default.right_marker,
) -> dict:
    """Patch a dictionary."""
    if not isinstance(input_dict, dict) or not isinstance(patch_dict, dict):
        raise CelsInputError(
            "Cels can only process input and patch documents in which the root element is a dictionary."
        )
    return patch_dictionary_rec(
        path=Path(),
        parent_patch=None,
        input_dict=input_dict,
        patch_dict=patch_dict,
        root_input_dict=input_dict,
        annotation_config=AnnotationConfig(
            separator, left_marker, index_marker, right_marker
        ),
    )


def patch_dictionary_rec(
    path: Path,
    parent_patch: Optional[Patch],
    input_dict: dict,
    patch_dict: dict,
    root_input_dict: dict,
    annotation_config: AnnotationConfig,
) -> dict:
    """Patch a dictionary (recursive function)."""

    # get patch for this dictionary
    patch = Patch(patch_dict, annotation_config, parent_patch, path)

    # create output dict
    output_dict = {}

    # process keys in input order
    for key, location in patch.get_keys(input_dict):
        # output dict value is only initialized if key in input dict
        if location != KeyLocation.only_patch:
            output_dict[key] = input_dict[key]

        # if only in input_dict, then nothing to process
        if location == KeyLocation.only_input:
            if _log_info_enabled:
                log.info(f"{path + key} [cyan]{{keep}}[/]", extra={"markup": True})
            continue

        # patch by applying all changes
        for change in patch[key]:
            result = change.apply(output_dict, key, patch, path, root_input_dict)

            # Optimize result type dispatch: the most common case is result
            # being None (set, delete, insert, extend, keep, etc.), so check
            # for that first with a simple truthiness test. Only then check
            # for the rarer signal types (CelsActionPatch, CelsActionRename).
            if result is None:
                continue
            if isinstance(result, _CelsActionPatch):
                result.tail_container[result.tail_index] = patch_dictionary_rec(
                    path=result.tail_path,
                    parent_patch=patch,
                    input_dict=result.input_dict,
                    patch_dict=result.patch_dict,
                    root_input_dict=root_input_dict,
                    annotation_config=annotation_config,
                )
            elif result is _CelsActionRename:
                output_dict[change.value] = output_dict[key]
                del output_dict[key]
                key = change.value

    return output_dict
