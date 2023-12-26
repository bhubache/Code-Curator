from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from manim import Arrow
from manim import Circle
from manim import Dot
from manim import DOWN
from manim import FadeIn
from manim import FadeOut
from manim import Rotate
from manim import Square
from manim import Text
from manim import UP
from manim.utils.testing.frames_comparison import frames_comparison

from code_curator.base_scene import BaseScene
from code_curator.utils.testing.curator_frames_comparison import curator_frames_comparison
from code_curator.utils.testing.curator_frames_comparison import starts_at

if TYPE_CHECKING:
    from manim import Mobject

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


@curator_frames_comparison(last_frame=False)
class test_introducing_one_mobject:
    def __init__(self, scene: BaseScene) -> None:
        self.scene = scene

    def fade_in_mobject(self):
        return FadeIn(Circle())


@curator_frames_comparison(last_frame=False)
class test_removing_one_mobject:
    def __init__(self, scene: BaseScene) -> None:
        self.scene = scene

    def fade_out_mobject(self):
        circle = Circle()
        self.scene.add(circle)

        return FadeOut(circle)


@curator_frames_comparison(last_frame=False)
class test_introducing_multiple_mobjects_at_the_same_time:
    def __init__(self, scene: BaseScene) -> None:
        self.scene = scene

    def fade_in_multiple_mobjects(self):
        return FadeIn(Circle()), FadeIn(Square().move_to((1, 1, 0)))


@curator_frames_comparison(last_frame=False)
class test_removing_multiple_mobjects_at_the_same_time:
    def __init__(self, scene: BaseScene) -> None:
        self.scene = scene

    def fade_out_multiple_mobjects(self):
        square = Square().move_to((1, 1, 0))
        circle = Circle()
        self.scene.add(square)
        self.scene.add(circle)

        return FadeOut(square), FadeOut(circle)


@curator_frames_comparison(last_frame=False)
class test_fade_in_and_fade_out_mobjects_at_the_same_time:
    def __init__(self, scene: BaseScene) -> None:
        self.scene = scene

    def animation(self):
        square = Square().move_to((1, 1, 0))
        self.scene.add(square)

        return FadeIn(Circle()), FadeOut(square)


@curator_frames_comparison(last_frame=False, run_time=1.5)
class test_overlapping_fade_in_animations_of_different_mobjects:
    def __init__(self, scene: BaseScene) -> None:
        self.scene = scene

    def first_fade_in(self):
        return FadeIn(Square().move_to((1, 1, 0)), run_time=1)

    @starts_at(0.5)
    def second_fade_in(self):
        return FadeIn(Circle())


@curator_frames_comparison(last_frame=False, run_time=1.5)
class test_overlapping_fade_out_animations_of_different_mobjects:
    def __init__(self, scene: BaseScene) -> None:
        self.scene = scene

    def first_fade_in(self):
        self.square = Square().move_to((1, 1, 0))
        self.circle = Circle()
        self.scene.add(self.square)
        self.scene.add(self.circle)

        return FadeOut(self.square)

    @starts_at(0.5)
    def second_fade_in(self):
        return FadeOut(self.circle)


@curator_frames_comparison(last_frame=False)
class test_fade_in_and_fade_out_different_mobjects_at_the_same_time:
    def __init__(self, scene: BaseScene) -> None:
        self.scene = scene

    def animation(self):
        square = Square().move_to((1, 1, 0))
        self.scene.add(square)

        return FadeIn(Circle()), FadeOut(square)


@curator_frames_comparison(last_frame=False, run_time=1.5)
class test_overlapping_fade_in_and_fade_out_different_mobjects:
    def __init__(self, scene: BaseScene) -> None:
        self.scene = scene

    def first_animation(self):
        square = Square().move_to((1, 1, 0))
        self.scene.add(square)

        return FadeOut(square)

    @starts_at(0.5)
    def second_animation(self):
        return FadeIn(Circle())


@curator_frames_comparison(last_frame=False)
@pytest.mark.skip(reason="Figure out what animations you would perform simultaneously")
class test_multiple_animations_on_one_mobject_at_the_same_time:
    def __init__(self, scene: BaseScene) -> None:
        self.scene = scene

    def animation(self):
        square = Square()
        self.scene.add(square)

        return Rotate(square), FadeOut(square)


@curator_frames_comparison(last_frame=False, run_time=1.5)
@pytest.mark.skip(reason="FIXME CUR-13")
class test_overlapping_animations_on_one_mobject:
    def __init__(self, scene: BaseScene) -> None:
        self.scene = scene

    def first_animation(self):
        self.circle = Circle()
        self.circle.set_opacity(0)
        self.scene.add(self.circle)

        return self.circle.animate.set_opacity(1)

    @starts_at(0.5)
    def second_animation(self):
        return self.circle.animate.to_edge(UP)


@curator_frames_comparison(last_frame=False, run_time=2)
class test_animations_that_start_at_the_same_time_but_have_different_run_times:
    def __init__(self, scene: BaseScene) -> None:
        self.scene = scene

    def first_animation(self):
        slow_square = Square().move_to((1, 1, 0))
        first_fast_square = Square().move_to((-1, 1, 0))
        self.second_fast_square = Square()

        self.scene.add(slow_square)
        self.scene.add(first_fast_square)
        self.scene.add(self.second_fast_square)

        return Rotate(slow_square, run_time=2), Rotate(first_fast_square)

    @starts_at(1.0)
    def second_animation(self):
        return Rotate(self.second_fast_square)


@curator_frames_comparison(last_frame=False)
class test_updater_works:
    def __init__(self, scene: BaseScene) -> None:
        self.scene = scene

    def animation(self):
        text = Text("This is a dot")
        dot = Dot()

        self.scene.add(text)
        self.scene.add(dot)

        def text_follow_dot_updater(mobject: Mobject):
            mobject.next_to(dot, DOWN)

        text.add_updater(text_follow_dot_updater, call_updater=True)

        return dot.animate.move_to((3, 3, 0))
