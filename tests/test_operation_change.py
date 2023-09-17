from cels.services import patch_dictionary


def test_operation_change_empty_list():
    input = {
        "foo": 100,
    }
    patch = {
        "foo {change}": [],
    }
    expected = {
        "foo": 100,
    }
    assert patch_dictionary(input, patch) == expected


def test_operation_change_delete_after_set():
    """Multiple operations for one key."""
    input = {
        "foo": 1,
    }
    patch = {
        "foo {change}": [
            {
                "operation": "set",
                "value": 2,
            },
            {
                "operation": "delete",
            },
        ]
    }
    expected = {}
    assert patch_dictionary(input, patch) == expected


def test_operation_change_set_after_delete():
    """Multiple operations for one key."""
    input = {
        "foo": 1,
    }
    patch = {
        "foo {change}": [
            {
                "operation": "delete",
            },
            {
                "operation": "set",
                "value": 2,
            },
        ]
    }
    expected = {
        "foo": 2,
    }
    assert patch_dictionary(input, patch) == expected


def test_operation_change_set_after_rename():
    """Multiple operations for one key."""
    input = {
        "foo": 1,
    }
    patch = {
        "foo {change}": [
            {
                "operation": "set",
                "value": 2,
            },
            {
                "operation": "rename",
                "value": "bar",
            },
        ]
    }
    expected = {
        "bar": 2,
    }
    assert patch_dictionary(input, patch) == expected


def test_operation_change_patch_after_rename():
    """Multiple operations for one key."""
    input = {
        "foo": {
            "bar": 1,
            "baz": 2,
        },
    }
    patch = {
        "foo {change}": [
            {
                "operation": "rename",
                "value": "spam",
            },
            {
                "operation": "patch",
                "value": {
                    "bar {rename}": "eggs",
                    "baz": 3,
                },
            },
        ]
    }
    expected = {
        "spam": {
            "eggs": 1,
            "baz": 3,
        },
    }
    assert patch_dictionary(input, patch) == expected


def test_operation_change_indices():
    input = {"foo": [[[100, 200]]]}
    patch = {
        "foo {change}": [{"operation": "set", "value": 300, "indices": [0, 0, 1]}],
    }
    expected = {"foo": [[[100, 300]]]}
    assert patch_dictionary(input, patch) == expected
