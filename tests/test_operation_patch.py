
import pytest

from patchwork.models import ChangeMap
from patchwork.services import patch_dict
from patchwork.errors import PatchworkInvalidPatch

def test_operation_patch_recursively():
    """Patch values recursively."""
    original = {
        "foo": {
            "bar": {
                "baz": {
                    "bat": 1
                },
            },
        },
    }
    patch = {
        "foo": {
            "bar": {
                "baz": {
                    "bat": 100
                },
            },
        },
    }
    expected = {
        "foo": {
            "bar": {
                "baz": {
                    "bat": 100
                },
            },
        },
    }
    assert patch_dict(original, patch) == expected

def test_operation_patch_explicitly():
    """Patch values recursively."""
    original = {
        "foo": {
            "bar": {
                "baz": {
                    "bat": 1
                },
            },
        },
    }
    patch = {
        "foo {patch}": {
            "bar {patch}": {
                "baz {patch}": {
                    "bat": 100
                },
            },
        },
    }
    expected = {
        "foo": {
            "bar": {
                "baz": {
                    "bat": 100
                },
            },
        },
    }
    assert patch_dict(original, patch) == expected


def test_operation_patch_non_annotated_key_non_dict_value():
    """Non annotated key whose original value is not a dict yields a 'set' operation."""
    original = {
        "foo": 1
    }
    patch = {
        "foo": {
            "bar": 1
        },
    }
    expected = {
        "foo": {
            "bar": 1
        },
    }
    assert patch_dict(original, patch) == expected

def test_operation_patch_non_dict_value():
    """It is not possible to patch an integer."""
    original = {
        "foo": 1
    }
    patch = {
        "foo {patch}": {
            "bar": 1
        },
    }
    with pytest.raises(PatchworkInvalidPatch):
        _ = patch_dict(original, patch)

def test_operation_patch_with_non_dict_value():
    """It is not possible to patch an integer."""
    original = {
        "foo": {
            "bar": 1
        },
    }
    patch = {
        "foo {patch}": 1
    }
    with pytest.raises(PatchworkInvalidPatch):
        _ = patch_dict(original, patch)

