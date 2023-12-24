from __future__ import annotations

import pytest

from code_curator.base_scene import BaseScene
from code_curator.base_scene import ExcludeDuplicationSubmobjectsMobject


@pytest.fixture
def base_scene_instance() -> BaseScene:
    return BaseScene()


# TODO CUR-1
#  1. Test descriptor get
#  2. Test descriptor set
#  3. Test descriptor delete
#  4. Test all base scene methods
#  5. Determine what methods on ExcludeDuplicateSubmobjectsMobject are needed


def test_getting_mobjects_returns_list_of_just_excluding_duplication_submobjects_mobject(base_scene_instance) -> None:
    correct_result = [ExcludeDuplicationSubmobjectsMobject()]

    # assert base_scene_instance.mobjects == correct_result
    assert len(base_scene_instance.mobjects) == 1
    assert isinstance(base_scene_instance.mobjects[0], ExcludeDuplicationSubmobjectsMobject)


def test_setting_mobjects_attribute_does_nothing(base_scene_instance) -> None:
    initial_mobjects = base_scene_instance.mobjects

    base_scene_instance.mobjects = []

    assert base_scene_instance.mobjects == initial_mobjects


def test_deleting_mobjects_attribute_raises_exception(base_scene_instance) -> None:
    with pytest.raises(AttributeError):
        del base_scene_instance.mobjects


def test_submobjects_is_initially_empty(base_scene_instance) -> None:
    assert len(base_scene_instance.submobjects) == 0
