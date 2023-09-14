import pytest

from patchwork.services import patch_dictionary
from patchwork.exceptions import PatchworkInputError


def test_operation_link_simple():
    """Link a scalar."""
    original = {
        "foo": {
            "bar": 3,
        },
    }
    patch = {
        "spam {link}": ".foo.bar",
    }
    expected = {
        "foo": {
            "bar": 3,
        },
        "spam": 3,
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_link_overwrite():
    """Link a scalar to an existing key."""
    original = {
        "foo": {
            "bar": 3,
        },
        "spam": {
            "eggs": 0,
        },
    }
    patch = {
        "spam": {
            "eggs {link}": ".foo.bar",
        },
    }
    expected = {
        "foo": {
            "bar": 3,
        },
        "spam": {
            "eggs": 3,
        },
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_link_dictionary():
    """Link a dictionary."""
    original = {
        "foo": {
            "bar": {
                "baz": 3,
            }
        },
    }
    patch = {
        "spam {link}": ".foo",
    }
    expected = {
        "foo": {
            "bar": {
                "baz": 3,
            }
        },
        "spam": {
            "bar": {
                "baz": 3,
            }
        },
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_link_list_element():
    """Link list element."""
    original = {
        "foo": {
            "bar": ["a", "b", "c"],
        },
    }
    patch = {
        "spam {link}": ".foo.bar[1]",
    }
    expected = {
        "foo": {
            "bar": ["a", "b", "c"],
        },
        "spam": "b",
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_link_list_element_with_deletion():
    """Link list element."""
    original = {
        "foo": {
            "bar": ["a", "b", "c"],
        },
    }
    patch = {
        "foo {delete}": None,
        "spam {link}": ".foo.bar[1]",
    }
    expected = {
        "spam": "b",
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_link_entire_document():
    """Link entire document."""
    original = {
        "foo": {
            "bar": ["a", "b", "c"],
        },
        "baz": 3,
    }
    patch = {
        "spam {link}": ".",
    }
    expected = {
        "foo": {
            "bar": ["a", "b", "c"],
        },
        "baz": 3,
        "spam": {
            "foo": {
                "bar": ["a", "b", "c"],
            },
            "baz": 3,
        },
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_empty_path():
    """Use empty path (link entire document)."""
    original = {
        "foo": {
            "bar": ["a", "b", "c"],
        },
        "baz": 3,
    }
    patch = {
        "spam {link}": "",
    }
    expected = {
        "foo": {
            "bar": ["a", "b", "c"],
        },
        "baz": 3,
        "spam": {
            "foo": {
                "bar": ["a", "b", "c"],
            },
            "baz": 3,
        },
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_wrong_path():
    """Use wrong path."""
    original = {
        "foo": {
            "bar": 3,
        },
    }
    patch = {
        "spam {link}": ".this.that",
    }
    with pytest.raises(PatchworkInputError):
        _ = patch_dictionary(original, patch)


def test_operation_wrong_path_type():
    """Use wrong path type."""
    original = {
        "foo": {
            "bar": 3,
        },
    }
    patch = {
        "spam {link}": 3,
    }
    with pytest.raises(PatchworkInputError):
        _ = patch_dictionary(original, patch)


def test_operation_wrong_path_type2():
    """Use wrong path type."""
    original = {
        "foo": {
            "bar": 3,
        },
    }
    patch = {
        "spam {link}": {"wrong": "path"},
    }
    with pytest.raises(PatchworkInputError):
        _ = patch_dictionary(original, patch)
