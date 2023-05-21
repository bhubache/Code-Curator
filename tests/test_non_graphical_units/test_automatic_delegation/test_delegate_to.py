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
        super().__init__()
        self._line = Line(color=Color('#FFFFFF'))


@pytest.fixture
def manim_delegate() -> ManimPropertyMobject:
    return ManimPropertyMobject()


def test_invalid_manim_property_delegate(manim_delegate: ManimPropertyMobject) -> None:
    with pytest.raises(KeyError):
        manim_delegate.invalid_manim_property_delegate


def test_valid_manim_property_delegate(manim_delegate: ManimPropertyMobject) -> None:
    assert manim_delegate.color == Color('#FFFFFF')


def test_valid_manim_property_delegate_assignment(manim_delegate: ManimPropertyMobject) -> None:
    manim_delegate.color = Color('#000000')
    assert manim_delegate.color == Color('#000000')


# TODO: Determine if manim properties can or cannot be deleted
# def test_valid_manim_property_delegate_deletion(manim_delegate: ManimPropertyMobject) -> None:
#     del manim_delegate.color
#     manim_delegate.color


def test_delegate_that_is_not_passed_to_delegate_to(manim_delegate: ManimPropertyMobject) -> None:
    with pytest.raises(AttributeError):
        manim_delegate.property_not_passed_in_to_delegate_to


class MobjectWithNonManimProperty(CustomVMobject):
    def __init__(self) -> None:
        super().__init__()
        self._non_manim_property: int = 5

    @property
    def non_manim_property(self) -> int:
        return self._non_manim_property

    @non_manim_property.setter
    def non_manim_property(self, new_value: int) -> None:
        self._non_manim_property = new_value

    @non_manim_property.deleter
    def non_manim_property(self) -> None:
        del self._non_manim_property


@delegate_to(
    MobjectWithNonManimProperty,
    to='_mobj',
    normal_include={
        '_non_manim_property',
    },
)
class DelegatingMobjectWithNonManimProperty(CustomVMobject):
    def __init__(self) -> None:
        super().__init__()
        self._mobj = MobjectWithNonManimProperty()


def test_mobj_with_non_manim_delegated_property_retrieval():
    obj = MobjectWithNonManimProperty()
    assert obj.non_manim_property == 5


def test_mobj_with_non_manim_delegated_property_assignment():
    obj = MobjectWithNonManimProperty()
    obj.non_manim_property = 100
    assert obj.non_manim_property == 100


def test_mobj_with_non_manim_delegated_property_deletion() -> None:
    obj = MobjectWithNonManimProperty()
    del obj.non_manim_property
