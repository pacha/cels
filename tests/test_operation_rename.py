from cels.services import patch_dictionary


def test_operation_rename():
    """Just a rename operation."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo {rename}": "bar",
    }
    expected = {
        "bar": 1,
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_rename_item_with_a_list_value():
    """Rename operation of a key from an item with a list value."""
    original = {
        "foo": [1, 2, 3],
    }
    patch = {
        "foo {rename}": "bar",
    }
    expected = {
        "bar": [1, 2, 3],
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_rename_key_in_nested_structure():
    original = {"foo": {"bar": {"baz": {"bat": 1}}}}
    patch = {"foo": {"bar": {"baz": {"bat {rename}": "spam"}}}}
    expected = {"foo": {"bar": {"baz": {"spam": 1}}}}
    assert patch_dictionary(original, patch) == expected


def test_operation_rename_with_non_string():
    """You can rename fields using any type."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo {rename}": 2,
    }
    expected = {2: 1}
    assert patch_dictionary(original, patch) == expected


def test_operation_rename_wrong_empty_string():
    """You can only rename fields using a non-empty string."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo {rename}": "",
    }
    expected = {"": 1}
    assert patch_dictionary(original, patch) == expected


def test_operation_rename_non_string_key():
    """Just a rename operation."""
    original = {
        "foo": "bar",
    }
    patch = {
        "foo {rename}": 2,
    }
    expected = {
        2: "bar",
    }
    assert patch_dictionary(original, patch) == expected
