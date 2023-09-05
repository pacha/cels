from inspect import cleandoc
from patchwork import patch_yaml


def test_yaml_set0():
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


def test_yaml_set1():
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


def test_yaml_set2():
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


def test_yaml_set3():
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


def test_yaml_set4():
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


def test_yaml_set5():
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


def test_yaml_set6():
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


def test_yaml_set7():
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


def test_yaml_set8():
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


def test_yaml_set9():
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


def test_yaml_set9():
    input = cleandoc(
        """

    foo:
      bar: 1
      baz: 2
    my_list:
    - foo
    - - one
      - - "up"
        - "mid"
        - "down"
      - three
    - baz
    spam: {"eggs": null}

    """
    )
    patch = cleandoc(
        """

    foo:
      baz: 100
    my_list {set@1, -2, 2}: 100
    spam: {"eggs": "a lot"}

    """
    )
    result = cleandoc(
        """

    foo:
      bar: 1
      baz: 100
    my_list:
    - foo
    - - one
      - - up
        - mid
        - 100
      - three
    - baz
    spam:
      eggs: a lot

    """
    )

    output = patch_yaml(input, patch).strip()
    assert output == result
