
import pytest

from patchwork.services import patch_dict
from patchwork.errors import PatchworkInvalidPatch

def test_operation_delete_scalar():
    """Just a delete operation."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo {delete}": None,
    }
    expected = {}
    assert patch_dict(original, patch) == expected

def test_operation_delete_list():
    """Delete operation for an item with a list value."""
    original = {
        "foo": [1, 2, 3],
    }
    patch = {
        "foo {delete}": None,
    }
    expected = {}
    assert patch_dict(original, patch) == expected

def test_operation_delete_non_none_value():
    """Deletion operations can't take any value other than None."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo {delete}": 2,
    }
    with pytest.raises(PatchworkInvalidPatch):
        _ = patch_dict(original, patch)

def test_operation_delete_nested():
    """Delete operation in a nested structure."""
    original = {
        "foo": {
            "bar": {
                "baz": {
                    "bat": ""
                }
            }
        }
    }
    patch = {
        "foo": {
            "bar": {
                "baz": {
                    "bat {delete}": None
                }
            }
        }
    }
    expected = {
        "foo": {
            "bar": {
                "baz": {
                }
            }
        }
    }
    assert patch_dict(original, patch) == expected

def test_operation_delete_list_element():
    """Delete operation of a list element."""
    original = {
        "foo": [1, 2, 3],
    }
    patch = {
        "foo {delete@1}": None,
    }
    expected = {
        "foo": [1, 3],
    }
    assert patch_dict(original, patch) == expected

def test_operation_delete_list_element_outside_bounds():
    """An outside bounds operation should raise an error"""
    original = {
        "foo": [1, 2, 3],
    }
    patch = {
        "foo {delete@5}": None,
    }
    with pytest.raises(PatchworkInvalidPatch):
        _ = patch_dict(original, patch)

