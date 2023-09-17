from cels.models import Patch


def test_patch_empty():
    """An empty patch dictionary generates an empty Patch."""
    raw_patch = {}
    patch = Patch(raw_patch)
    assert patch.data == {}


def test_patch_minimal():
    """An empty patch dictionary generates an empty Patch."""
    raw_patch = {
        "foo": 1,
    }
    patch = Patch(raw_patch)
    assert list(patch.data.keys()) == ["foo"]
    assert len(patch["foo"]) == 1
    assert patch["foo"][0].operation is None
    assert patch["foo"][0].value == 1
    assert patch["foo"][0].indices == []
