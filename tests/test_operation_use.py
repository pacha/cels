from cels.services import patch_dictionary


def test_operation_use_simple():
    """Use a variable."""
    original = {}
    patch = {
        "foo {var}": 100,
        "bar {use}": "foo",
    }
    expected = {
        "bar": 100,
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_use_overwrite():
    """Use a variable to overwrite a value."""
    original = {
        "bar": 0,
    }
    patch = {
        "foo {var}": 100,
        "bar {use}": "foo",
    }
    expected = {
        "bar": 100,
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_use_dictionary():
    """Use a dictionary variable."""
    original = {}
    patch = {
        "foo {var}": {
            "spam": {
                "eggs": 100,
            },
        },
        "bar {use}": "foo",
    }
    expected = {
        "bar": {
            "spam": {
                "eggs": 100,
            },
        },
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_use_from_previous_scope():
    """Use a variable defined in grand-parent directory."""
    original = {}
    patch = {
        "foo {var}": 100,
        "spam": {
            "eggs": {
                "bar {use}": "foo",
            },
        },
    }
    expected = {
        "spam": {
            "eggs": {
                "bar": 100,
            },
        },
    }
    assert patch_dictionary(original, patch) == expected
