from inspect import cleandoc

from patchwork import patch_json


def test_json_multiple_changes(fixtures_path):
    input_path = fixtures_path / "full-example-json" / "input.json"
    input = cleandoc(input_path.read_text())
    patch_path = fixtures_path / "full-example-json" / "patch.json"
    patch = cleandoc(patch_path.read_text())
    result_path = fixtures_path / "full-example-json" / "result.json"
    result = cleandoc(result_path.read_text())

    output = patch_json(input, patch).strip()
    assert output == result
