from __future__ import annotations

import pytest
from manim import Square

from code_curator.base_scene import BaseScene
from code_curator.base_scene import TopLevelBaseSceneMobject


@pytest.fixture
def base_scene_instance() -> BaseScene:
    return BaseScene()


def test_getting_mobjects_attribute_returns_list_of_just_top_level_base_scene_mobject(base_scene_instance) -> None:
    assert len(base_scene_instance.mobjects) == 1
    assert isinstance(base_scene_instance.mobjects[0], TopLevelBaseSceneMobject)


def test_setting_mobjects_attribute_does_nothing(base_scene_instance) -> None:
    initial_mobjects = base_scene_instance.mobjects

    base_scene_instance.mobjects = []

    assert base_scene_instance.mobjects == initial_mobjects


def test_deleting_mobjects_attribute_raises_exception(base_scene_instance) -> None:
    with pytest.raises(AttributeError):
        del base_scene_instance.mobjects


def test_submobjects_is_initially_empty(base_scene_instance) -> None:
    assert len(base_scene_instance.submobjects) == 0


def test_adding_mobject_to_scene(base_scene_instance) -> None:
    square = Square()
    base_scene_instance.add(square)

    assert len(base_scene_instance.mobjects) == 1
    assert len(base_scene_instance.submobjects) == 1
    assert base_scene_instance.submobjects[0] == square


def test_adding_duplicate_mobject_to_scene_does_not_add_duplicate(base_scene_instance) -> None:
    square = Square()

    base_scene_instance.add(square)
    base_scene_instance.add(square)

    assert len(base_scene_instance.mobjects) == 1
    assert len(base_scene_instance.submobjects) == 1
    assert base_scene_instance.submobjects[0] == square


def test_clearing_scene_mobjects(base_scene_instance) -> None:
    base_scene_instance.add(Square())

    base_scene_instance.clear()

    assert len(base_scene_instance.mobjects) == 1
    assert len(base_scene_instance.submobjects) == 0
    assert isinstance(base_scene_instance.mobjects[0], TopLevelBaseSceneMobject)
