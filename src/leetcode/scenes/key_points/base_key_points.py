from __future__ import annotations

from manim import FadeIn
from manim import UP
from script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript

from .base_scene import BaseScene
from .problem_setup.problem_text import ProblemText


class BaseKeyPoints(BaseScene):
    # config.background_color = '#000E15'

    def __init__(
        self,
        points: list[str],
        insights: list[str],
        problem_dir: str,
        aligned_animation_scene: CompositeAnimationScript,
    ) -> None:
        BaseScene.__init__(self, problem_dir=problem_dir)
        self._points: list[str] = points
        self._insights: list[str] = insights

    def setup(self):
        super().setup()

    def construct(self):
        pass

    def tear_down(self):
        super().tear_down()

    def animate_key_points_setup(self):
        header = ProblemText.create_title('Key Points')
        header.to_edge(UP)

        animations = []
        animations.append(FadeIn(header))

        # self._key_points_table = ProblemText.create_key_points_table()
