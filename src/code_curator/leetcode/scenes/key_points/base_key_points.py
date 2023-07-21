from __future__ import annotations

import inspect

from manim import AnimationGroup
from manim import FadeIn
from manim import UP
from code_curator.script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript

from code_curator.base_scene import BaseScene
from ...problem_text import ProblemText


class BaseKeyPoints(BaseScene):
    # config.background_color = '#000E15'

    def __init__(
        self,
        points: list[str],
        insights: list[str],
        problem_dir: str,
        aligned_animation_scene: CompositeAnimationScript,
    ) -> None:
        BaseScene.__init__(self, problem_dir=problem_dir, aligned_animation_scene=aligned_animation_scene)
        self._points: list[str] = points
        self._insights: list[str] = insights

        self._key_points_table = ProblemText.create_key_points_table(self._points, self._insights)
        self._animation_spec = self.create_animation_spec()
        self.add_base_animations()

    def __getattr__(self, attr_name):
        section_name = inspect.stack()[1].function
        subsection_name = '_'.join(attr_name.split('_')[:-1])
        subsection_number = attr_name.split('_')[-1]
        print(self.aligned_animation_scene.unique_id)
        animation_leaf = self.aligned_animation_scene.get_component(f'{section_name}_{subsection_number}')
        # result = self.aligned_animation_scene.get_child(section_name)
        timing_info = getattr(animation_leaf, animation_leaf.SUBANIMATION_TIMINGS_NAME)
        # if attr_name == 'curve_pointer_1':
        #     breakpoint()
        return timing_info[subsection_name].copy()
        # print(result)
        # raise
        # return result
        # return getattr(self.aligned_animation_scene, attr_name)

    def create_animation_spec(self):
        return {
            'intro': self.animate_key_points_setup(),
            **self._init_key_points_animations(),
        }

    def _init_key_points_animations(self):
        key_points_dict = {}
        for index in range(1, len(self._insights) + 1):
            if index == 0:
                continue

            key_points_dict[f'key_point_{index}_fade_in'] = self._present_single_problem_explanation(index=index)

        return key_points_dict

    def _present_single_problem_explanation(self, index):
        def inner():
            opacity_fade_in_animation = self._get_key_point_explanations()[index].animate.set_opacity(1)
            opacity_fade_in_animation.run_time = 1
            return [opacity_fade_in_animation]
        return inner

    def _get_key_point_explanations(self):
        return self._key_points_table.get_columns()[1]

    def add_overriding_animation(self, method):
        self._aligned_animation_scene.add_animation(unique_id=method.__name__, func=method, animation=method(), is_overriding_animation=True)

    def animate_key_points_setup(self):
        def inner():
            header = ProblemText.create_title('Key Points')
            header.to_edge(UP)

            animations = []
            animations.append(FadeIn(header))
            animations.append(FadeIn(self._key_points_table))

            return [AnimationGroup(*animations)]
        return inner

        # self._key_points_table = ProblemText.create_key_points_table()
