from typing import Optional

from cels import default
from cels.logs import log
from cels.models import Path
from cels.models import Patch
from cels.models import KeyLocation
from cels.models import AnnotationConfig
from cels.exceptions import CelsInputError
from cels.exceptions import CelsActionPatch
from cels.exceptions import CelsActionRename


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
            log.info(f"{path + key} [cyan]{{keep}}[/]", extra={"markup": True})
            continue

        # patch by applying all changes
        for change in patch[key]:
            try:
                change.apply(output_dict, key, patch, path, root_input_dict)
            except CelsActionPatch as exc:
                exc.tail_container[exc.tail_index] = patch_dictionary_rec(
                    path=exc.tail_path,
                    parent_patch=patch,
                    input_dict=exc.input_dict,
                    patch_dict=exc.patch_dict,
                    root_input_dict=root_input_dict,
                    annotation_config=annotation_config,
                )
            except CelsActionRename:
                output_dict[change.value] = output_dict[key]
                del output_dict[key]
                key = change.value

    return output_dict
