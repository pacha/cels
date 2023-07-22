
import logging as log
import pytest

from patchwork.models import ChangeMap
from patchwork.services import patch_dict
from patchwork.errors import PatchworkInvalidPatch

def test_operation_insert_at_start():
    """Insert element at the start of a list."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {insert@0}": 100,
    }
    expected = {
        "foo": [100, 1, 2, 3, 4, 5],
    }
    assert patch_dict(original, patch) == expected

def test_operation_insert_in_between():
    """Insert element in the middle of a list."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {insert@3}": 100,
    }
    expected = {
        "foo": [1, 2, 3, 100, 4, 5],
    }
    assert patch_dict(original, patch) == expected

def test_operation_insert_at_end():
    """Insert element at the end of a list."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {insert}": 100,
    }
    expected = {
        "foo": [1, 2, 3, 4, 5, 100],
    }
    assert patch_dict(original, patch) == expected

def test_operation_insert_negative_index():
    """Insert element using a negative index."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {insert@-1}": 100,
    }
    expected = {
        "foo": [1, 2, 3, 4, 100, 5],
    }
    assert patch_dict(original, patch) == expected

def test_operation_insert_negative_index_again():
    """Insert element using a negative index."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {insert@-3}": 100,
    }
    expected = {
        "foo": [1, 2, 100, 3, 4, 5],
    }
    assert patch_dict(original, patch) == expected

def test_operation_insert_out_of_bounds():
    """Insert element in an out-of-bounds position."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {insert@5}": 100,
    }
    with pytest.raises(PatchworkInvalidPatch):
        _ = patch_dict(original, patch)

def test_operation_insert_out_of_bounds_negative_index():
    """Insert element in an out-of-bounds position."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {insert@-6}": 100,
    }
    with pytest.raises(PatchworkInvalidPatch):
        _ = patch_dict(original, patch)

