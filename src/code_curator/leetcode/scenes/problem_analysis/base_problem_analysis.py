from __future__ import annotations

from typing import TYPE_CHECKING

from manim import AnimationGroup
from manim import FadeIn
from manim import UP

from code_curator.base_scene import BaseScene
from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.leetcode.problem_text import ProblemText


if TYPE_CHECKING:
    from collections.abc import Sequence
    from manim import MobjectTable
    from code_curator.script_handling.components.animation_script.composite_animation_script import (  # noqa: E501
        CompositeAnimationScript,
    )


logger = CustomLogger.getLogger(__name__)


class BaseProblemAnalysis(BaseScene):
    def __init__(
        self,
        constraints: Sequence[str],
        explanations: Sequence[str],
        problem_dir: str,
        aligned_animation_scene: CompositeAnimationScript,
        **kwargs,
    ):
        super().__init__(
            problem_dir=problem_dir,
            aligned_animation_scene=aligned_animation_scene,
            **kwargs,
        )
        self._constraints_list = constraints
        self._explanations = explanations
        self._problem_dir = problem_dir
        self._aligned_animation_scene = aligned_animation_scene
        self._title = ProblemText.create_title("Constraints Analysis")
        self._constraints_analysis_table: MobjectTable = (
            ProblemText.create_constraints_table(
                self._constraints_list,
                self._explanations,
            )
        )

    def fade_in_table(self):
        self._title.to_edge(UP)

        yield AnimationGroup(
            FadeIn(self._title),
            FadeIn(self._constraints_analysis_table),
        )

    def show_constraint_one_explanation(self):
        # TODO: Make an "attribute animation" that can take in a string like
        #  "opacity" and animate it's change so I don't have to use
        #  the animate attribute
        yield self._get_constraint_explanations(1).animate.set_opacity(1)

    def _get_constraint_explanations(self, num: int):
        return self._constraints_analysis_table.get_columns()[1][num - 1]

    def _init_constraints_animations(self):
        constraints_dict = {}
        for index in range(1, len(self._explanations) + 1):
            if index == 0:
                continue

            constraints_dict[f"explanation_{index}_fade_in"] = (
                self._present_single_problem_explanation(index=index)
            )

        return constraints_dict

    # NOTE: I've monkey patched a run_time attribute to this AnimationBuilder
    def _present_single_problem_explanation(self, index):
        def inner():
            opacity_fade_in_animation = self._get_constraint_explanations()[
                index
            ].animate.set_opacity(1)
            opacity_fade_in_animation.run_time = 1
            return [opacity_fade_in_animation]

        return inner
