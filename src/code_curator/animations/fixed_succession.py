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
    """Enables multiple animations of the same mobject in one Scene.play() call."""

    def __init__(self, *animations: Animation) -> None:
        self.group = Group(*[anim.mobject for anim in animations])
        super().__init__(
            mobject=self.group,
            run_time=self._get_run_time(animations),
        )
        self.animations: tuple[Animation] = self._translate_remove_animations(list(animations))
        self.mobjects_to_remove = [anim.mobject for anim in animations if anim.is_remover()]

    def begin(self):
        for anim in self.animations:
            if not isinstance(anim, FadeOut):
                anim.begin()

        super().begin()

    def interpolate(self, alpha) -> None:
        animation, corrected_alpha = self._get_animation_and_corrected_alpha(alpha)
        animation.interpolate(smooth(corrected_alpha))

    def clean_up_from_scene(self, scene: Scene):
        for mobject in self.mobjects_to_remove:
            scene.remove(mobject)

    def _get_animation_and_corrected_alpha(self, alpha: float) -> Animation:
        for index, (lower_bound, upper_bound) in self.animation_alpha_range_map.items():
            if lower_bound <= alpha < upper_bound or (lower_bound <= alpha <= upper_bound and upper_bound == 1.0):
                return self.animations[index], ((alpha - lower_bound) / (upper_bound - lower_bound))

        raise ValueError(f'Unable to find corresponding animation for alpha {alpha}')

    @cached_property
    def animation_alpha_range_map(self) -> dict[int, tuple[float, float]]:
        soft_max_alphas = self._soft_max(self.animations)

        alpha_ranges = {}
        alpha_sum = 0.0

        for i, curr_alpha in enumerate(soft_max_alphas):
            alpha_ranges[i] = (alpha_sum, alpha_sum := alpha_sum + curr_alpha)

        return alpha_ranges

    def _get_run_time(self, animations: tuple[Animation]) -> float:
        """Get total run time for animations.

        Args:
            animations: Animations to be played successively.

        Returns:
            total_run_time: Total run time of animations.
        """
        total_run_time: float = 0.0
        for anim in animations:
            total_run_time += anim.run_time

        return total_run_time

    def _soft_max(self, animations: Sequence[Animation]) -> list[float]:
        return [anim.run_time / self.run_time for anim in animations]

    def _translate_remove_animations(self, animations: list[Animation]) -> tuple[Animation]:
        """Enable FadeOut animations to occur successfully."""
        for i, anim in enumerate(animations):
            if isinstance(anim, FadeOut):
                def interpolate(alpha: float, anim: Animation = anim) -> None:
                    """Enable proper fade out for all mobjects that do so.

                    Due to late binding closures, you cannot do the following

                    .. code:: python

                        anim.interpolate = lambda alpha: anim.mobject.fade(alpha)

                    because for all animations that this assignment happens to, anim
                    will just refer to the last animation in ``animations``.
                    """
                    anim.mobject.fade(alpha)

                anim.interpolate = interpolate

        return tuple(animations)
