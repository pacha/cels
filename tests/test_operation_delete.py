import pytest

from cels.services import patch_dictionary
from cels.exceptions import CelsInputError


def test_operation_delete_scalar():
    """Just a delete operation."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo {delete}": None,
    }
    expected = {}
    assert patch_dictionary(original, patch) == expected


def test_operation_delete_scalar_ignoring_value():
    """Just a delete operation. Any value provided is ignored."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo {delete}": [1, 2, 3],
    }
    expected = {}
    assert patch_dictionary(original, patch) == expected


def test_operation_delete_list():
    """Delete operation for an item with a list value."""
    original = {
        "foo": [1, 2, 3],
    }
    patch = {
        "foo {delete}": None,
    }
    expected = {}
    assert patch_dictionary(original, patch) == expected


def test_operation_delete_nested():
    """Delete operation in a nested structure."""
    original = {"foo": {"bar": {"baz": {"bat": ""}}}}
    patch = {"foo": {"bar": {"baz": {"bat {delete}": None}}}}
    expected = {"foo": {"bar": {"baz": {}}}}
    assert patch_dictionary(original, patch) == expected


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
    assert patch_dictionary(original, patch) == expected
