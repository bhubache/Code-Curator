from manim import *

from ..base_scene import BaseScene
from ..problem_text import ProblemText
from .scene_scheduler import SceneScheduler

from .scene_scheduler import OverridingAnimationInfo

import json

from typing import Iterable

class BaseProblemAnalysis(BaseScene):
    def __init__(self, constraints, explanations, problem_dir, aligned_animation_script):
        BaseScene.__init__(self, problem_dir=problem_dir)
        self._constraints_list = constraints
        self._explanations = explanations
        self._problem_dir = problem_dir
        self._aligned_animation_script = aligned_animation_script
        self._title = ProblemText.create_title('Constraints Analysis')
        self._constraints_analysis_table = ProblemText.create_constraints_table(self._constraints_list, self._explanations)

        self._animation_spec = {
            'intro': {
                'pre': None,
                'during': self.animate_analysis_setup,
                'post': None
            },
            'explanation': {
                'pre': None,
                'during': self._init_constraints_animations(),
                'post': None
            }
        }

        self._scene_scheduler = SceneScheduler(animation_spec=self._animation_spec, aligned_animation_script=self._aligned_animation_script)

    def setup(self):
        # Schedule entire scene here
        self._animations = self._scene_scheduler.schedule()

        for i, obj in enumerate(self._animations):
            if isinstance(obj, OverridingAnimationInfo):
                self._animations[i] = super().add_overriding_animation(obj)

    def construct(self):
        for i, obj in enumerate(self._animations):
            if isinstance(obj, list):
                for anim in obj:
                    print(anim.run_time)
                    self.play(anim)
            elif isinstance(obj, Animation):
                print(obj.run_time)
                self.play(obj)
            else:
                obj()
        # self._run_animations()

    def tear_down(self):
        super().tear_down()

    def _get_animation_spec_key_path(self, method) -> Iterable[str]:
        parts = method.__name__.split('_')
        keys = []
        if parts[0] == 'intro':
            keys.append(parts[0])
            if parts[1] == 'pre':
                raise NotImplementedError('pre animation of the intro section is not implemented in animation_scheduler')
            elif parts[1] == 'during':
                raise ValueError('The \'during\' animation for the intro is reserved for fading in the constraints table')
            elif parts[1] == 'post':
                raise NotImplementedError('post animation of the intro section is not implemented in animation_scheduler')
        elif parts[0] == 'explanation':
            keys.append(parts[0])
            if parts[1] == 'pre':
                raise NotImplementedError('pre animation of the explanation section is not implemented in animation_scheduler')
            if parts[1].isnumeric():
                keys.append('during')
                explanation_num_key = int(parts[1])
                keys.append(explanation_num_key)
                keys.append(parts[2])
            elif parts[1] == 'post':
                raise NotImplementedError('post animation of the intro section is not implemented in animation_scheduler')
        
        return keys

    def _schedule_scene(self):
        pass

    def _set_nested_dict(self, keys: Iterable[str], d: str, value):
        for level in keys[:-1]:
            d = d[level]
        d[keys[-1]] = value

    def add_overriding_animation(self, method):
        keys = self._get_animation_spec_key_path(method)
        method.__dict__['is_overriding_animation'] = True
        self._set_nested_dict(keys, value=method, d=self._animation_spec)

    def _run_animations(self, animation_spec = None):
        if animation_spec is None:
            animation_spec = self._animation_spec
        for section, animation_chunk in animation_spec.items():
            for order, animation in animation_chunk.items():
                if animation is None: continue

                if isinstance(animation, dict):
                    self._run_animations(animation)
                    continue

                anim_obj = animation()
                if anim_obj is not None:
                    self.play(anim_obj)

    def _init_constraints_animations(self):
        constraints_dict = {}
        for index in range(1, len(self._explanations) + 1):
            if index == 0: continue
            constraints_dict[index] = {
                'pre': None,
                'during': self._present_single_problem_explanation(index=index),
                'post': None
            }
        return constraints_dict

    def _present_single_problem_explanation(self, index):
        def inner():
            return [self._get_constraint_explanations()[index].animate.set_opacity(1)]
        return inner

    def animate_analysis_setup(self):
        self._title.to_edge(UP)

        animations = []
        animations.append(FadeIn(self._title))
        animations.append(FadeIn(self._constraints_analysis_table))
        # return AnimationGroup(*animations)
        return [AnimationGroup(*animations)]

    def _get_constraint_explanations(self):
        return self._constraints_analysis_table.get_columns()[1]