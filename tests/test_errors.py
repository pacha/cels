import pytest

from patchwork.services import patch_dictionary
from patchwork.exceptions import PatchworkInputError
from patchwork.logs import log


def test_wrong_operation():
    original = {}
    patch = {
        "foo {bar}": None,
    }
    with pytest.raises(PatchworkInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_operation_delete_from_empty_dict():
    original = {}
    patch = {
        "foo {delete}": None,
    }
    with pytest.raises(PatchworkInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_operation_delete_non_existent():
    original = {
        "bar": 1,
        "baz": 2,
    }
    patch = {
        "foo {delete}": None,
    }
    with pytest.raises(PatchworkInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_operation_delete_from_empty_list():
    original = {
        "foo": [],
    }
    patch = {
        "foo {delete@3}": None,
    }
    with pytest.raises(PatchworkInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_operation_delete_out_of_bounds():
    original = {
        "foo": ["a", "b", "c"],
    }
    patch = {
        "foo {delete@3}": None,
    }
    with pytest.raises(PatchworkInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])
