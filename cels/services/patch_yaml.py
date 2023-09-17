from .patch_document import patch_document


def patch_yaml(input_text: str, patch_text: str) -> str:
    return patch_document(
        input_format="yaml",
        input_text=input_text,
        patch_format="yaml",
        patch_text=patch_text,
        output_format="yaml",
    )
