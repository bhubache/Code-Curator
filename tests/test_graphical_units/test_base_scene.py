from __future__ import annotations

import pytest
from manim import Arrow
from manim import Circle
from manim import Square
from manim.utils.testing.frames_comparison import frames_comparison

from code_curator.base_scene import BaseScene

__module_test__ = "base_scene"


@frames_comparison(base_scene=BaseScene)
def test_initial_base_scene_is_blank(scene: BaseScene) -> None:
    ...


@frames_comparison(base_scene=BaseScene)
def test_adding_mobject_to_scene_makes_it_appear_on_screen(scene: BaseScene) -> None:
    scene.add(Square())


@frames_comparison(base_scene=BaseScene)
def test_adding_multiple_mobjects_to_scene_makes_them_appear_on_screen(scene: BaseScene) -> None:
    scene.add(Square())
    scene.add(Circle().move_to((2, 2, 0)))
    scene.add(Arrow().move_to((-2, -2, 0)))


@frames_comparison(base_scene=BaseScene)
@pytest.mark.skip(reason="FIXME CUR-10")
def test_removing_mobject_from_scene_makes_it_disappear_from_screen(scene: BaseScene) -> None:
    square = Square()
    scene.add(square)

    scene.remove(square)


@frames_comparison(base_scene=BaseScene)
def test_clearing_scene_makes_all_mobjects_disappear_from_screen(scene: BaseScene) -> None:
    scene.add(Square())
    scene.add(Circle().move_to((2, 2, 0)))
    scene.add(Arrow().move_to((-2, -2, 0)))

    scene.clear()
