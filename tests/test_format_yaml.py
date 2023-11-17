from inspect import cleandoc

from cels import patch_yaml


def test_yaml_empty():
    input = cleandoc(
        """
    """
    )
    patch = cleandoc(
        """
    """
    )
    result = cleandoc(
        """
    {}
    """
    )

    output = patch_yaml(input, patch).strip()
    assert output == result


def test_yaml_only_input():
    input = cleandoc(
        """

    foo: 1

    """
    )
    patch = cleandoc(
        """
    """
    )
    result = cleandoc(
        """

    foo: 1

    """
    )

    output = patch_yaml(input, patch).strip()
    assert output == result


def test_yaml_only_patch():
    input = cleandoc(
        """
    """
    )
    patch = cleandoc(
        """

    foo: 1

    """
    )
    result = cleandoc(
        """

    foo: 1

    """
    )

    output = patch_yaml(input, patch).strip()
    assert output == result


def test_yaml_overwrite():
    input = cleandoc(
        """

    foo: 1

    """
    )
    patch = cleandoc(
        """

    foo: 2

    """
    )
    result = cleandoc(
        """

    foo: 2

    """
    )

    output = patch_yaml(input, patch).strip()
    assert output == result


def test_yaml_compose():
    input = cleandoc(
        """

    foo: 1
    bar: 2

    """
    )
    patch = cleandoc(
        """

    foo: 1
    baz: 3

    """
    )
    result = cleandoc(
        """

    foo: 1
    bar: 2
    baz: 3

    """
    )

    output = patch_yaml(input, patch).strip()
    assert output == result


def test_yaml_nested_dict():
    input = cleandoc(
        """

    foo:
      bar: 1

    """
    )
    patch = cleandoc(
        """

    foo:
      bar: 2

    """
    )
    result = cleandoc(
        """

    foo:
      bar: 2

    """
    )

    output = patch_yaml(input, patch).strip()
    assert output == result


def test_yaml_nested_dicts():
    input = cleandoc(
        """

    foo:
      bar:
        baz: 1

    """
    )
    patch = cleandoc(
        """

    foo:
      bar:
        baz: 2

    """
    )
    result = cleandoc(
        """

    foo:
      bar:
        baz: 2

    """
    )

    output = patch_yaml(input, patch).strip()
    assert output == result


def test_yaml_list_overwrite():
    input = cleandoc(
        """

    my_list:
      - foo
      - bar
      - baz

    """
    )
    patch = cleandoc(
        """

    my_list: 100

    """
    )
    result = cleandoc(
        """

    my_list: 100

    """
    )

    output = patch_yaml(input, patch).strip()
    assert output == result


def test_yaml_list_set():
    input = cleandoc(
        """

    my_list:
    - foo
    - bar
    - baz

    """
    )
    patch = cleandoc(
        """

    my_list {set@1}: 100

    """
    )
    result = cleandoc(
        """

    my_list:
    - foo
    - 100
    - baz

    """
    )

    output = patch_yaml(input, patch).strip()
    assert output == result


def test_yaml_nested_list_set():
    input = cleandoc(
        """

    my_list:
    - foo
    - - one
      - two
      - three
    - baz

    """
    )
    patch = cleandoc(
        """

    my_list {set@1,1}: 100

    """
    )
    result = cleandoc(
        """

    my_list:
    - foo
    - - one
      - 100
      - three
    - baz

    """
    )

    output = patch_yaml(input, patch).strip()
    assert output == result


def test_yaml_nested_list_set_negative_index():
    input = cleandoc(
        """

    my_list:
    - foo
    - - one
      - two
      - three
    - baz

    """
    )
    patch = cleandoc(
        """

    my_list {set@1,-2}: 100

    """
    )
    result = cleandoc(
        """

    my_list:
    - foo
    - - one
      - 100
      - three
    - baz

    """
    )

    output = patch_yaml(input, patch).strip()
    assert output == result


def test_yaml_empty_annotation():
    input = cleandoc(
        """

    foo:
      bar: 1
      baz: 2

    """
    )
    patch = cleandoc(
        """

    foo {}:
      baz: 100
    """
    )
    result = cleandoc(
        """

    foo:
      bar: 1
      baz: 100
    """
    )

    output = patch_yaml(input, patch).strip()
    assert output == result


def test_yaml_multiple_changes(fixtures_path):
    input_path = fixtures_path / "full-example-yaml" / "input.yaml"
    input = cleandoc(input_path.read_text())
    patch_path = fixtures_path / "full-example-yaml" / "patch.yaml"
    patch = cleandoc(patch_path.read_text())
    result_path = fixtures_path / "full-example-yaml" / "result.yaml"
    result = cleandoc(result_path.read_text())

    output = patch_yaml(input, patch).strip()
    assert output == result


def test_yaml_special_chars():
    input = cleandoc(
        """

    Name: "María"
    Straße: "221B Baker Street"

    """
    )
    patch = cleandoc(
        """
    Name: "Jörg"
    """
    )
    result = cleandoc(
        """

    Name: Jörg
    Straße: 221B Baker Street

    """
    )

    output = patch_yaml(input, patch).strip()
    assert output == result
