from cels.services import patch_dictionary


def test_operation_patch_recursively():
    """Patch values recursively."""
    original = {
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
        "foo": {
            "bar": {
                "baz": {"bat": 100},
            },
        },
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_patch_explicitly():
    """Patch values recursively."""
    original = {
        "foo": {
            "bar": {
                "baz": {"bat": 1},
            },
        },
    }
    patch = {
        "foo {patch}": {
            "bar {patch}": {
                "baz {patch}": {"bat": 100},
            },
        },
    }
    expected = {
        "foo": {
            "bar": {
                "baz": {"bat": 100},
            },
        },
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_patch_non_annotated_key_non_dict_value():
    """Non annotated key whose original value is not a dict yields a 'set' operation."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo": {"bar": 1},
    }
    expected = {
        "foo": {"bar": 1},
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_patch_non_dict_value():
    """It is not possible to patch an integer."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo {patch}": {"bar": 1},
    }
    expected = {
        "foo": {"bar": 1},
    }
    assert patch_dictionary(original, patch) == expected
