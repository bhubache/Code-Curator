from __future__ import annotations

import pytest
from automatic_delegation.delegate_to import delegate_to
from colour import Color
from manim import Line

from src.custom_vmobject import CustomVMobject


@delegate_to(
    Line,
    to='_line',
    manim_property_include={
        'color',
        'invalid_manim_property_delegate',
    },
)
class ManimPropertyMobject(CustomVMobject):
    def __init__(self) -> None:
        self._line = Line(color=Color('#FFFFFF'))
        # self._non_manim_property = 0

    # @property
    # def color(self) -> Color:
    #     return self._line.color

    # @color.setter
    # def color(self, new_color: str | Color) -> None:
    #     self._line.color = new_color


@pytest.fixture
def manim_delegate() -> ManimPropertyMobject:
    return ManimPropertyMobject()


def test_invalid_manim_property_delegate(manim_delegate: ManimPropertyMobject) -> None:
    with pytest.raises(KeyError):
        manim_delegate.invalid_manim_property_delegate


def test_delegate_that_is_not_passed_to_delegate_to(manim_delegate: ManimPropertyMobject) -> None:
    pass


# def test_delegate_missing_manim_property() -> None:
#     with pytest.raises(Exception):
#         manim_property_mobject = ManimPropertyMobject()


# def test_valid_delegate() -> None:
#     manim_property_mobject = ManimPropertyMobject()
#     assert manim_property_mobject.stroke_width == 100

def test_color_delegate() -> None:
    manim_property_mobject = ManimPropertyMobject()
    assert manim_property_mobject.color == Color('#FFFFFF')


def test_another_delegate() -> None:
    manim_property_mobject = ManimPropertyMobject()
    assert manim_property_mobject.color == Color('#FFFFFF')
