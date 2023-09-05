
import pytest

from patchwork.services import patch_dictionary
from patchwork.exceptions import PatchworkInputError


def test_operation_change_wrong_value():
    """The value in a change operation must be a list."""
    input = {
        "foo": 1,
    }
    patch = {
        "foo {change}": {
            "operation": "set",
            "value": 2,
        },
    }
    with pytest.raises(PatchworkInputError):
        _ = patch_dictionary(input, patch)

def test_operation_change_wrong_operation():
    """The value in a change operation must be a list."""
    input = {
        "foo": 1,
    }
    patch = {
        "foo {change}": [
            {
                "this": "is not a valid operation",
            }
        ]
    }
    with pytest.raises(PatchworkInputError):
        _ = patch_dictionary(input, patch)

def test_operation_change_delete_after_set():
    """Multiple operations for one key."""
    input = {
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
    assert patch_dictionary(input, patch) == expected

def test_operation_change_set_after_delete():
    """Multiple operations for one key."""
    input = {
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
    assert patch_dictionary(input, patch) == expected

def test_operation_change_set_after_rename():
    """Multiple operations for one key."""
    input = {
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
    assert patch_dictionary(input, patch) == expected

def test_operation_change_patch_after_rename():
    """Multiple operations for one key."""
    input = {
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
    assert patch_dictionary(input, patch) == expected
