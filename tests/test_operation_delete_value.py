import pytest

from cels.services import patch_dictionary
from cels.exceptions import CelsInputError


def test_operation_delete_value_single():
    original = {
        "foo": [1, 2, 3],
    }
    patch = {
        "foo {delete_value}": 2,
    }
    expected = {
        "foo": [1, 3],
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_delete_value_complex():
    original = {
        "foo": [1, {"foo": 1, "bar": 2}, 3],
    }
    patch = {
        "foo {delete_value}": {"foo": 1, "bar": 2},
    }
    expected = {
        "foo": [1, 3],
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_delete_value_in_nested_list():
    original = {
        "foo": [100, [1, 2, 3], 200],
    }
    patch = {
        "foo {delete_value@1}": 2,
    }
    expected = {
        "foo": [100, [1, 3], 200],
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_delete_value_all_occurrences():
    original = {
        "foo": [1, 2, 3, 2],
    }
    patch = {
        "foo {delete_value}": 2,
    }
    expected = {
        "foo": [1, 3],
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_delete_value_from_non_list():
    original = {
        "foo": 2,
    }
    patch = {
        "foo {delete_value}": 2,
    }
    with pytest.raises(CelsInputError):
        _ = patch_dictionary(original, patch)


def test_operation_delete_value_non_occurring():
    original = {
        "foo": [1, 2, 3, 2],
    }
    patch = {
        "foo {delete_value}": 4,
    }
    expected = {
        "foo": [1, 2, 3, 2],
    }
    assert patch_dictionary(original, patch) == expected
