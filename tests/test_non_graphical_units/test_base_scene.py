from __future__ import annotations

import pytest
from manim import Square

from code_curator.base_scene import BaseScene
from code_curator.base_scene import ExcludeDuplicationSubmobjectsMobject


def test_exclude_duplicate_submobjects_mobject_is_singleton() -> None:
    assert ExcludeDuplicationSubmobjectsMobject() is ExcludeDuplicationSubmobjectsMobject()


def test_exclude_duplicate_submobjects_mobject_submobjects_do_not_clear_upon_instantations() -> None:
    mobject = ExcludeDuplicationSubmobjectsMobject()
    mobject.add(Square())

    same_mobject = ExcludeDuplicationSubmobjectsMobject()
    assert len(same_mobject.submobjects) == 1
    assert isinstance(same_mobject.submobjects[0], Square)


# TODO CUR-1
#  1. Test descriptor get
#  2. Test descriptor set
#  3. Test descriptor delete
#  4. Test all base scene methods
#  5. Determine what methods on ExcludeDuplicateSubmobjectsMobject are needed


def test_initial_base_scene_state() -> None:
    base_scene = BaseScene()

    assert base_scene.mobjects == [ExcludeDuplicationSubmobjectsMobject()]


# def test_descriptor_get_is_consistent() -> None:
#     base_scene = BaseScene()
#     assert base_scene.mobjects == base_scene.mobjects


def test_setting_mobjects_attribute_does_nothing() -> None:
    base_scene = BaseScene()
    initial_mobjects = base_scene.mobjects

    base_scene.mobjects = []

    assert base_scene.mobjects == initial_mobjects


def test_deleting_mobjects_attribute_raises_exception() -> None:
    base_scene = BaseScene()

    with pytest.raises(AttributeError):
        del base_scene.mobjects
