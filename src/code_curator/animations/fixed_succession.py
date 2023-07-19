from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from manim import Animation
from manim import FadeOut
from manim import Group
from manim import smooth

if TYPE_CHECKING:
    from collections.abc import Sequence
    from manim import Scene


class FixedSuccession(Animation):
    def __init__(self, *animations):
        self.group = Group(*[anim.mobject for anim in animations])
        super().__init__(
            mobject=self.group,
            run_time=self._get_run_time(animations),
        )
        self.animations = self._translate_remove_animations(list(animations))
        self.mobjects_to_remove = [anim.mobject for anim in animations if anim.is_remover()]

    def begin(self):
        for anim in self.animations:
            if not isinstance(anim, FadeOut):
                anim.begin()

        super().begin()

    def interpolate(self, alpha):
        animation, corrected_alpha = self._get_animation_and_corrected_alpha(alpha)
        animation.interpolate(smooth(corrected_alpha))

    def clean_up_from_scene(self, scene):
        for mobject in self.mobjects_to_remove:
            scene.remove(mobject)

    def _get_animation_and_corrected_alpha(self, alpha):
        for index, (lower_bound, upper_bound) in self.animation_alpha_range_map.items():
            if lower_bound <= alpha < upper_bound or (lower_bound <= alpha <= upper_bound and upper_bound == 1.0):
                return self.animations[index], ((alpha - lower_bound) / (upper_bound - lower_bound))
            
        raise ValueError()
    
    @cached_property
    def animation_alpha_range_map(self):
        soft_max_alphas = self._soft_max(self.animations)

        alpha_ranges = {}
        alpha_sum = 0.0

        for i, curr_alpha in enumerate(soft_max_alphas):
            alpha_ranges[i] = (alpha_sum, alpha_sum := alpha_sum + curr_alpha)

        return alpha_ranges
    
    def _get_run_time(self, animations):
        total_run_time = 0.0
        for anim in animations:
            total_run_time += anim.run_time

        return total_run_time
    
    def _soft_max(self, animations):
        return [anim.run_time / self.run_time for anim in animations]
    
    def _translate_remove_animations(self, animations):
        for i, anim in enumerate(animations):
            if isinstance(anim, FadeOut):
                def interpolate(alpha, anim = anim):
                    anim.mobject.fade(alpha)

                anim.interpolate = interpolate
        return tuple(animations)