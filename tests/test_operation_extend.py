
import logging as log
import pytest

from patchwork.models import ChangeMap
from patchwork.services import patch_dict
from patchwork.errors import PatchworkInvalidPatch

def test_operation_extend_at_start():
    """Extend at the start of a list."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {extend@0}": ["a", "b"],
    }
    expected = {
        "foo": ["a", "b", 1, 2, 3, 4, 5],
    }
    assert patch_dict(original, patch) == expected

def test_operation_extend_in_between():
    """Extend in the middle of a list."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {extend@3}": ["a", "b"],
    }
    expected = {
        "foo": [1, 2, 3, "a", "b", 4, 5],
    }
    assert patch_dict(original, patch) == expected

def test_operation_extend_at_end():
    """Extend at the end of a list."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {extend}": ["a", "b"],
    }
    expected = {
        "foo": [1, 2, 3, 4, 5, "a", "b"],
    }
    assert patch_dict(original, patch) == expected

def test_operation_extend_negative_index():
    """Extend using a negative index."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {extend@-1}": ["a", "b"],
    }
    expected = {
        "foo": [1, 2, 3, 4, "a", "b", 5],
    }
    assert patch_dict(original, patch) == expected


def test_operation_extend_negative_index_again():
    """Extend using a negative index."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {extend@-3}": ["a", "b"],
    }
    expected = {
        "foo": [1, 2, "a", "b", 3, 4, 5],
    }
    assert patch_dict(original, patch) == expected

def test_operation_extend_empty_list():
    """Extend an empty list."""
    original = {
        "foo": [],
    }
    patch = {
        "foo {extend}": ["a", "b"],
    }
    expected = {
        "foo": ["a", "b"],
    }
    assert patch_dict(original, patch) == expected

def test_operation_extend_empty_list_with_index():
    """Extend an empty list using an index."""
    original = {
        "foo": [],
    }
    patch = {
        "foo {extend@0}": ["a", "b"],
    }
    expected = {
        "foo": ["a", "b"],
    }
    assert patch_dict(original, patch) == expected

def test_operation_extend_empty_list_with_negative_index():
    """Extend an empty list using a negative index."""
    original = {
        "foo": [],
    }
    patch = {
        "foo {extend@-1}": ["a", "b"],
    }
    expected = {
        "foo": ["a", "b"],
    }
    assert patch_dict(original, patch) == expected

def test_operation_extend_empty_list_with_wrong_index():
    """Extend an empty list using a wrong index."""
    original = {
        "foo": [],
    }
    patch = {
        "foo {extend@1}": ["a", "b"],
    }
    with pytest.raises(PatchworkInvalidPatch):
        _ = patch_dict(original, patch)

def test_operation_extend_empty_list_with_empty_list():
    """Extend an empty list with an empty list."""
    original = {
        "foo": [],
    }
    patch = {
        "foo {extend}": [],
    }
    expected = {
        "foo": [],
    }
    assert patch_dict(original, patch) == expected

def test_operation_extend_out_of_bounds():
    """Extend with an out-of-bounds position."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {extend@5}": ["a", "b"],
    }
    with pytest.raises(PatchworkInvalidPatch):
        _ = patch_dict(original, patch)

def test_operation_extend_out_of_bounds_negative_index():
    """Extend with an out-of-bounds position."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {extend@-6}": ["a", "b"],
    }
    with pytest.raises(PatchworkInvalidPatch):
        _ = patch_dict(original, patch)

def test_operation_extend_with_non_list():
    """Extend with an out-of-bounds position."""
    original = {
        "foo": "bar",
    }
    patch = {
        "foo {extend@2}": ["a", "b"],
    }
    with pytest.raises(PatchworkInvalidPatch):
        _ = patch_dict(original, patch)

