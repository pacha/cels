from cels.services import patch_dictionary


def test_operation_set_new():
    """Add a new item."""
    original = {}
    patch = {
        "foo": 100,
    }
    expected = {
        "foo": 100,
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_set_add_to_existing():
    """Add a new item."""
    original = {
        "foo": 1,
    }
    patch = {
        "bar": 2,
    }
    expected = {
        "foo": 1,
        "bar": 2,
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_set_non_string_keys():
    """Add a new item."""
    original = {
        1: "foo",
    }
    patch = {
        1: "bar",
    }
    expected = {
        1: "bar",
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_set_new_explicit():
    """Add a new item with an explicit annotation."""
    original = {}
    patch = {
        "foo {set}": 100,
    }
    expected = {
        "foo": 100,
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_set_override_value():
    """Override previous value."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo": 100,
    }
    expected = {
        "foo": 100,
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_set_override_value_explicit():
    """Override previous value with an explicit annotation."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo {set}": 100,
    }
    expected = {
        "foo": 100,
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_set_override_different_type():
    """Override value of different type."""
    original = {
        "foo": "bar",
    }
    patch = {
        "foo": 100,
    }
    expected = {
        "foo": 100,
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_set_override_different_type_explicit():
    """Override value of different type with an explitic annotation."""
    original = {
        "foo": "bar",
    }
    patch = {
        "foo {set}": 100,
    }
    expected = {
        "foo": 100,
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_set_override_nested_value():
    """Override nested value."""
    original = {
        "spam": "eggs",
        "foo": {
            "bar": {
                "baz": {"bat": 1},
            },
        },
    }
    patch = {
        "foo": {
            "bar": {
                "baz": {"bat": 100},
            },
        },
    }
    expected = {
        "spam": "eggs",
        "foo": {
            "bar": {
                "baz": {"bat": 100},
            },
        },
    }
    assert patch_dictionary(original, patch) == expected
