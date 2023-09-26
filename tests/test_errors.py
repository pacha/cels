import pytest

from cels.logs import log
from cels.services import patch_dictionary
from cels.exceptions import CelsInputError


def test_error_wrong_operation():
    original = {}
    patch = {
        "foo {bar}": None,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_delete_from_empty_dict():
    original = {}
    patch = {
        "foo {delete}": None,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_delete_non_existent():
    original = {
        "bar": 1,
        "baz": 2,
    }
    patch = {
        "foo {delete}": None,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_delete_from_empty_list():
    original = {
        "foo": [],
    }
    patch = {
        "foo {delete@3}": None,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_delete_out_of_bounds():
    original = {
        "foo": ["a", "b", "c"],
    }
    patch = {
        "foo {delete@3}": None,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_set_index_for_scalar():
    original = {
        "foo": 3,
    }
    patch = {
        "foo {set@2}": 100,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_set_string_index():
    original = {
        "foo": [1, 2, 3],
    }
    patch = {
        "foo {set@bar}": 100,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_set_negative_index_for_dict():
    original = {
        "foo": {
            "bar": 1,
            "baz": 2,
        },
    }
    patch = {
        "foo {set@-1}": 100,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_set_with_underscore():
    """Set operation with an underscore in indices."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {set@_}": 100,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_underscore_not_at_last_position():
    original = {
        "foo": [1, ["a", [100, 200], "b"], 3, 4, 5],
    }
    patch = {
        "foo {insert@1,_,1}": 300,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_index_provided_for_operation_without_index():
    original = {
        "foo": [1, ["a", [100, 200], "b"], 3, 4, 5],
    }
    patch = {
        "foo {rename@1}": "bar",
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_annotation_after_set():
    original = {
        "foo": 100,
    }
    patch = {
        "foo {set}": {
            "bar": {
                "baz {link}": "foo",
            },
        },
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_change_wrong_type():
    original = {
        "foo": 100,
    }
    patch = {
        "foo {change}": 200,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_change_wrong_value():
    """The value in a change operation must be a list."""
    original = {
        "foo": 1,
    }
    patch = {
        "foo {change}": {
            "operation": "set",
            "value": 2,
        },
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_change_missing_operation():
    original = {
        "foo": 1,
    }
    patch = {
        "foo {change}": [
            {
                "this": "is not a valid operation",
            }
        ]
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_change_wrong_operation():
    original = {
        "foo": 1,
    }
    patch = {
        "foo {change}": [
            {
                "operation": "is not a valid operation",
            }
        ]
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_change_missing_value():
    original = {
        "foo": 1,
    }
    patch = {
        "foo {change}": [
            {
                "operation": "set",
            }
        ]
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_change_wrong_index_type():
    original = {
        "foo": 1,
    }
    patch = {
        "foo {change}": [
            {
                "operation": "rename",
                "value": "bar",
                "indices": "3, 4",
            }
        ]
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_change_wrong_index_elements():
    original = {
        "foo": 1,
    }
    patch = {
        "foo {change}": [
            {
                "operation": "rename",
                "value": "bar",
                "indices": ["3", "4"],
            }
        ]
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_change_index_in_wrong_operation():
    original = {
        "foo": 1,
    }
    patch = {
        "foo {change}": [
            {
                "operation": "rename",
                "value": "bar",
                "indices": [3, 4],
            }
        ]
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_change_extra_field():
    original = {
        "foo": [1, 2, 3],
    }
    patch = {
        "foo {change}": [
            {
                "operation": "set",
                "value": 100,
                "indices": [1],
                "spam": "eggs",
            }
        ]
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_extend_empty_list_with_negative_index():
    """Extend an empty list using a negative index."""
    original = {
        "foo": [],
    }
    patch = {
        "foo {extend@-1}": ["a", "b"],
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_extend_empty_list_with_wrong_index():
    """Extend an empty list using a wrong index."""
    original = {
        "foo": [],
    }
    patch = {
        "foo {extend@1}": ["a", "b"],
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_extend_out_of_bounds():
    """Extend with an out-of-bounds position."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {extend@5}": ["a", "b"],
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_extend_out_of_bounds_negative_index():
    """Extend with an out-of-bounds position."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {extend@-6}": ["a", "b"],
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_extend_with_non_list():
    """Extend with an out-of-bounds position."""
    original = {
        "foo": "bar",
    }
    patch = {
        "foo {extend@2}": ["a", "b"],
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_extend_using_non_list_value():
    original = {
        "foo": [],
    }
    patch = {
        "foo {extend}": "a",
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_extend_targeting_non_list_value():
    original = {
        "foo": 1,
    }
    patch = {
        "foo {extend}": ["a"],
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_insert_out_of_bounds():
    """Insert element in an out-of-bounds position."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {insert@5}": 100,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_insert_out_of_bounds_negative_index():
    """Insert element in an out-of-bounds position."""
    original = {
        "foo": [1, 2, 3, 4, 5],
    }
    patch = {
        "foo {insert@-6}": 100,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_insert_into_non_list():
    original = {
        "foo": 1,
    }
    patch = {
        "foo {insert}": 100,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_insert_into_non_list_using_index():
    original = {
        "foo": 1,
    }
    patch = {
        "foo {insert@5}": 100,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_wrong_path():
    """Use wrong path."""
    original = {
        "foo": {
            "bar": 3,
        },
    }
    patch = {
        "spam {link}": ".this.that",
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_wrong_path_random_string():
    """Use wrong path."""
    original = {
        "foo": {
            "bar": 3,
        },
    }
    patch = {
        "spam {link}": "&)$(/(·",
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_wrong_path_type():
    """Use wrong path type."""
    original = {
        "foo": {
            "bar": 3,
        },
    }
    patch = {
        "spam {link}": 3,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_wrong_path_type_dict():
    """Use wrong path type."""
    original = {
        "foo": {
            "bar": 3,
        },
    }
    patch = {
        "spam {link}": {"wrong": "path"},
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_patch_with_non_dict_value():
    """It is not possible to patch an integer."""
    original = {
        "foo": {"bar": 1},
    }
    patch = {"foo {patch}": 1}
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_set_no_annotations_in_value_overriding():
    """The patch value should not have annotations in a set operation."""
    original = {"this": {"foo": 1}}
    patch = {
        "this": {
            "foo {set}": {"bar {set}": 2},
        },
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_render_wrong_template():
    original = {}
    patch = {
        "foo {var}": 100,
        "bar {render}": "{{ foo }",
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_render_empty_template():
    original = {}
    patch = {
        "foo {var}": 100,
        "bar {render}": "{{}}",
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_render_non_existing_filter():
    original = {}
    patch = {
        "foo {var}": 100,
        "bar {render}": "{{ foo|madeup }}",
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_use_non_defined_variable():
    original = {}
    patch = {
        "foo {var}": 100,
        "bar {use}": "baz",
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_delete_list_element_outside_bounds():
    """An outside bounds operation should raise an error"""
    original = {
        "foo": [1, 2, 3],
    }
    patch = {
        "foo {delete@5}": None,
    }
    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])


def test_error_list_as_root():
    """The root element must be a dictionary."""
    original = [1, 2, 3]
    patch = {}

    with pytest.raises(CelsInputError) as err:
        _ = patch_dictionary(original, patch)
    log.info(err.value.args[0])
