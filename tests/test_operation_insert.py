from cels.services import patch_dictionary


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
    assert patch_dictionary(original, patch) == expected


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
    assert patch_dictionary(original, patch) == expected


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
    assert patch_dictionary(original, patch) == expected


def test_operation_insert_at_end_with_underscore():
    """Insert element at the end of a list using an underscore."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {insert@_}": 100,
    }
    expected = {
        "foo": [1, 2, 3, 4, 5, 100],
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_insert_at_nested_list():
    """Insert element at the end of a nested list using an underscore."""
    original = {
        "foo": [1, ["a", [100, 200], "b"], 3, 4, 5],
    }
    patch = {
        "foo {insert@1,1}": 300,
    }
    expected = {
        "foo": [1, ["a", 300, [100, 200], "b"], 3, 4, 5],
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_insert_at_nested_list_end_with_underscore():
    """Insert element at the end of a nested list using an underscore."""
    original = {
        "foo": [1, ["a", [100, 200], "b"], 3, 4, 5],
    }
    patch = {
        "foo {insert@1,1,_}": 300,
    }
    expected = {
        "foo": [1, ["a", [100, 200, 300], "b"], 3, 4, 5],
    }
    assert patch_dictionary(original, patch) == expected


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
    assert patch_dictionary(original, patch) == expected


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
    assert patch_dictionary(original, patch) == expected
