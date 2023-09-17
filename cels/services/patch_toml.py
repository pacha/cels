from .patch_document import patch_document


def patch_toml(input_text: str, patch_text: str) -> str:
    return patch_document(
        input_format="toml",
        input_text=input_text,
        patch_format="toml",
        patch_text=patch_text,
        output_format="toml",
    )
