from manim import *

from base_scene import BaseScene
from leetcode.problem_text import ProblemText

import json

from typing import Iterable

class BaseProblemAnalysis(BaseScene):
    def __init__(self, constraints, explanations, problem_dir, aligned_animation_scene):
        BaseScene.__init__(self, problem_dir=problem_dir, aligned_animation_scene=aligned_animation_scene)
        self._constraints_list = constraints
        self._explanations = explanations
        self._problem_dir = problem_dir
        self._aligned_animation_scene = aligned_animation_scene
        self._title = ProblemText.create_title('Constraints Analysis')
        self._constraints_analysis_table = ProblemText.create_constraints_table(self._constraints_list, self._explanations)
        self._animation_spec = self.create_animation_spec()

    def setup(self):
        super().setup()

    def construct(self):
        super().construct()

    def tear_down(self):
        super().tear_down()

    def create_animation_spec(self):
        spec = {
            'intro': self.animate_analysis_setup(),
            **self._init_constraints_animations()
            }
        return spec

    # NOTE: Strange behavior where super class add_overriding_animation method was being called in super class, but this one here was being invoked instead
    def add_overriding_animation(self, method):
        if not self._aligned_animation_scene.add_animations(unique_id=method.__name__, animations=method(), is_overriding_animation=True):
            raise RuntimeError(f'Unable to find {method.__name__}')

    def _init_constraints_animations(self):
        constraints_dict = {}
        for index in range(1, len(self._explanations) + 1):
            if index == 0: continue
            constraints_dict[f'explanation_{index}_fade_in'] = self._present_single_problem_explanation(index=index)
        return constraints_dict

    # NOTE: I've monkey patched a run_time attribute to this AnimationBuilder
    def _present_single_problem_explanation(self, index):
        opacity_fade_in_animation = self._get_constraint_explanations()[index].animate.set_opacity(1)
        opacity_fade_in_animation.run_time = 1
        return [opacity_fade_in_animation]
    # def _present_single_problem_explanation(self, index):
    #     def inner():
    #         return [self._get_constraint_explanations()[index].animate.set_opacity(1)]
    #     return inner

    def animate_analysis_setup(self):
        self._title.to_edge(UP)

        animations = []
        animations.append(FadeIn(self._title))
        animations.append(FadeIn(self._constraints_analysis_table))
        return [AnimationGroup(*animations)]

    def _get_constraint_explanations(self):
        return self._constraints_analysis_table.get_columns()[1]