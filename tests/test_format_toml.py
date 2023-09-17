from inspect import cleandoc

from cels import patch_toml


def test_toml_multiple_changes(fixtures_path):
    input_path = fixtures_path / "full-example-toml" / "input.toml"
    input = cleandoc(input_path.read_text())
    patch_path = fixtures_path / "full-example-toml" / "patch.toml"
    patch = cleandoc(patch_path.read_text())
    result_path = fixtures_path / "full-example-toml" / "result.toml"
    result = cleandoc(result_path.read_text())

    output = patch_toml(input, patch).strip()
    assert output == result
