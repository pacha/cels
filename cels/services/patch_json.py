from .patch_document import patch_document


def patch_json(input_text: str, patch_text: str) -> str:
    return patch_document(
        input_format="json",
        input_text=input_text,
        patch_format="json",
        patch_text=patch_text,
        output_format="json",
    )
