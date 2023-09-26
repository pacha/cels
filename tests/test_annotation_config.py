from typing import Union
from dataclasses import dataclass

import pytest

from cels.models import AnnotationConfig
from cels.exceptions import CelsInputError


@dataclass
class Example:
    text: str
    separator: str
    left_marker: str
    right_marker: str
    match: Union[str, None] = None


correct_annotation_list = [
    Example(
        text="field {}",
        separator=" ",
        left_marker="{",
        right_marker="}",
        match="",
    ),
    Example(
        text="field {operation}",
        separator=" ",
        left_marker="{",
        right_marker="}",
        match="operation",
    ),
    Example(
        text="field {operation@1}",
        separator=" ",
        left_marker="{",
        right_marker="}",
        match="operation@1",
    ),
    Example(
        text="field {operation@-1}",
        separator=" ",
        left_marker="{",
        right_marker="}",
        match="operation@-1",
    ),
    Example(
        text="f {operation@-100}",
        separator=" ",
        left_marker="{",
        right_marker="}",
        match="operation@-100",
    ),
    Example(
        text="f {o@0}", separator=" ", left_marker="{", right_marker="}", match="o@0"
    ),
    Example(
        text="fie{ld {operation}",
        separator=" ",
        left_marker="{",
        right_marker="}",
        match="operation",
    ),
    Example(
        text="fie {ld} {operation}",
        separator=" ",
        left_marker="{",
        right_marker="}",
        match="operation",
    ),
    Example(
        text="fie _operation_",
        separator=" ",
        left_marker="_",
        right_marker="_",
        match="operation",
    ),
    Example(
        text="fie_operation_",
        separator="",
        left_marker="_",
        right_marker="_",
        match="operation",
    ),
    Example(
        text="fie {{operation}}",
        separator=" ",
        left_marker="{{",
        right_marker="}}",
        match="operation",
    ),
    Example(
        text="fie__operation",
        separator="__",
        left_marker="",
        right_marker="",
        match="operation",
    ),
    Example(
        text="fie __operation__",
        separator=" ",
        left_marker="__",
        right_marker="__",
        match="operation",
    ),
    Example(
        text="fie _|operation|_",
        separator=" ",
        left_marker="_|",
        right_marker="|_",
        match="operation",
    ),
    Example(
        text="fie [operation]",
        separator=" ",
        left_marker="[",
        right_marker="]",
        match="operation",
    ),
    Example(
        text="fie (operation)",
        separator=" ",
        left_marker="(",
        right_marker=")",
        match="operation",
    ),
    Example(
        text="fie operation",
        separator=" ",
        left_marker="",
        right_marker="",
        match="operation",
    ),
    Example(
        text="fie @operation>",
        separator=" ",
        left_marker="@",
        right_marker=">",
        match="operation",
    ),
    Example(
        text="fie <operation@",
        separator=" ",
        left_marker="<",
        right_marker="@",
        match="operation",
    ),
    Example(
        text="f @operation@-100>",
        separator=" ",
        left_marker="@",
        right_marker=">",
        match="operation@-100",
    ),
]

non_annotation_list = [
    Example(text="{operation}", separator=" ", left_marker="{", right_marker="}"),
    Example(text="field{operation}", separator=" ", left_marker="{", right_marker="}"),
    Example(
        text="field{operation@1}", separator=" ", left_marker="{", right_marker="}"
    ),
    Example(text="fie _operation_", separator=" ", left_marker="{", right_marker="}"),
    Example(text="fie _operation", separator=" ", left_marker="_", right_marker="_"),
]


@pytest.fixture(params=correct_annotation_list)
def correct_annotation(request):
    return request.param


@pytest.fixture(params=non_annotation_list)
def non_annotation(request):
    return request.param


def test_annotation_correct_annotations(correct_annotation):
    """Check keys with correct annotations."""
    annotation_config = AnnotationConfig(
        separator=correct_annotation.separator,
        left_marker=correct_annotation.left_marker,
        right_marker=correct_annotation.right_marker,
    )
    match = annotation_config.regex.match(correct_annotation.text)
    assert match
    assert match.group(2) == correct_annotation.match


def test_annotation_non_annotations(non_annotation):
    """Check keys that are not annotated."""
    annotation_config = AnnotationConfig(
        separator=non_annotation.separator,
        left_marker=non_annotation.left_marker,
        right_marker=non_annotation.right_marker,
    )
    assert not annotation_config.regex.match(non_annotation.text)
