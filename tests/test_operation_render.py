from cels.services import patch_dictionary


def test_operation_render_simple():
    """Render a variable."""
    original = {}
    patch = {
        "foo {var}": 100,
        "bar {render}": "{{ foo }}",
    }
    expected = {
        "bar": "100",
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_render_simple2():
    """Render a variable with a prefix."""
    original = {}
    patch = {
        "foo {var}": "some-id",
        "bar {render}": "some-prefix-{{ foo }}",
    }
    expected = {
        "bar": "some-prefix-some-id",
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_render_override_value():
    """Render a variable with a prefix and override an existing variable."""
    original = {
        "bar": 0,
    }
    patch = {
        "foo {var}": "some-id",
        "bar {render}": "some-prefix-{{ foo }}",
    }
    expected = {
        "bar": "some-prefix-some-id",
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_render_value_from_dict():
    """Render a value from a dictionary."""
    original = {}
    patch = {
        "foo {var}": {
            "spam": {"eggs": ["a0", "a1", "a2"]},
        },
        "bar {render}": "some-prefix-{{ foo.spam.eggs[1] }}",
    }
    expected = {
        "bar": "some-prefix-a1",
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_render_use_filter():
    """Render a variable making it uppercase."""
    original = {}
    patch = {
        "foo {var}": "some-id",
        "bar {render}": "some-prefix-{{ foo|upper }}",
    }
    expected = {
        "bar": "some-prefix-SOME-ID",
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_render_in_nested_list():
    """Render a variable with a prefix."""
    original = {
        "bar": [[["a0", "a2", "a3"], ["b0", "b2", "b3"]], 0],
    }
    patch = {
        "foo {var}": "some-id",
        "bar {render@0,1,1}": "some-prefix-{{ foo }}",
    }
    expected = {
        "bar": [[["a0", "a2", "a3"], ["b0", "some-prefix-some-id", "b3"]], 0],
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_render_dict():
    """Render a full dictionary instead of a scalar."""
    original = {}
    patch = {
        "foo {var}": {
            "bar": {"baz": 100},
        },
        "bar {render}": "{{ foo }}",
    }
    expected = {
        "bar": "{'bar': {'baz': 100}}",
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_render_built_in_filter():
    """Render a full dictionary instead of a scalar."""
    original = {}
    patch = {
        "foo {var}": [1, 2, 3, 4],
        "bar {render}": "{{ foo|sum }}",
    }
    expected = {
        "bar": "10",
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_render_get_function():
    """Retrieve a value from the original dictionary using the provided _get function."""
    original = {
        "foo": 100,
    }
    patch = {
        "bar {render}": "The value is {{ _get('.foo') }}",
    }
    expected = {
        "foo": 100,
        "bar": "The value is 100",
    }
    assert patch_dictionary(original, patch) == expected


def test_operation_render_get_function_with_nested_list():
    """Retrieve a value from the original dictionary using the provided _get function."""
    original = {
        "section": ["foo", "bar"],
    }
    patch = {
        "section {render@1}": "{{ _get('.section[1]') | upper }}",
    }
    expected = {
        "section": ["foo", "BAR"],
    }
    assert patch_dictionary(original, patch) == expected
