from cels.services import patch_dictionary


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
    assert patch_dictionary(original, patch) == expected


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
    assert patch_dictionary(original, patch) == expected


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
    assert patch_dictionary(original, patch) == expected


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
    assert patch_dictionary(original, patch) == expected


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
    assert patch_dictionary(original, patch) == expected


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
    assert patch_dictionary(original, patch) == expected


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
    assert patch_dictionary(original, patch) == expected


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
    assert patch_dictionary(original, patch) == expected
