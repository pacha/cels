import pytest

from patchwork.models import ChangeMap
from patchwork.services import patch_dict
from patchwork.errors import PatchworkInvalidPatch


def test_operation_change():
    """Annotations are just a shorthand for writing change operations."""
    original = {
        "foo": 1,
    }

    # create change map from annotated patch
    data_annotation = {
        "foo {set}": 2,
    }
    change_map_annotation = ChangeMap(original, data_annotation)

    # create change map using the change operation
    data_change = {
        "foo {change}": [{
            "operation": "set",
            "value": 2,
        }]
    }
    change_map_change = ChangeMap(original, data_change)

    assert change_map_annotation.changes == change_map_change.changes

def test_operation_change_wrong_value():
    """The value in a change operation must be a list."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo {change}": {
            "operation": "set",
            "value": 2,
        },
    }
    with pytest.raises(PatchworkInvalidPatch):
        _ = patch_dict(original, patch)

def test_operation_change_wrong_operation():
    """The value in a change operation must be a list."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo {change}": [
            {
                "this": "is not a valid operation",
            }
        ]
    }
    with pytest.raises(PatchworkInvalidPatch):
        _ = patch_dict(original, patch)

def test_operation_change_delete_after_set():
    """Multiple operations for one key."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo {change}": [
            {
                "operation": "set",
                "value": 2,
            },
            {
                "operation": "delete",
            },
        ]
    }
    expected = {
    }
    assert patch_dict(original, patch) == expected

def test_operation_change_set_after_delete():
    """Multiple operations for one key."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo {change}": [
            {
                "operation": "delete",
            },
            {
                "operation": "set",
                "value": 2,
            },
        ]
    }
    expected = {
        "foo": 2,
    }
    assert patch_dict(original, patch) == expected

def test_operation_change_set_after_rename():
    """Multiple operations for one key."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo {change}": [
            {
                "operation": "set",
                "value": 2,
            },
            {
                "operation": "rename",
                "value": "bar",
            },
        ]
    }
    expected = {
        "bar": 2,
    }
    assert patch_dict(original, patch) == expected

def test_operation_change_patch_after_rename():
    """Multiple operations for one key."""
    original = {
        "foo": {
            "bar": 1,
            "baz": 2,
        },
    }
    patch = {
        "foo {change}": [
            {
                "operation": "rename",
                "value": "spam",
            },
            {
                "operation": "patch",
                "value": {
                    "bar {rename}": "eggs",
                    "baz": 3,
                },
            },
        ]
    }
    expected = {
        "spam": {
            "eggs": 1,
            "baz": 3,
        },
    }
    assert patch_dict(original, patch) == expected

