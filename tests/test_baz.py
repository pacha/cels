import pytest

from patchwork.app import Baz


def test_model():
    baz = Baz.from_dict({"spam": "a"})
    assert baz.eggs == "aaa"
