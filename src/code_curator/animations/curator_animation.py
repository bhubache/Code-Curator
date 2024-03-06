from __future__ import annotations

import collections
from collections.abc import Iterable
from typing import Callable
from typing import TYPE_CHECKING

from manim import Animation
from manim import prepare_animation

from .utils.math_ import value_from_range_to_range
from code_curator.animations.composition import CuratorAnimationGroup

if TYPE_CHECKING:
    from collections.abc import Sequence


class CuratorAnimation(Animation):
    def __init__(self, mobject, animation_script, scene, run_time: float) -> None:
        super().__init__(mobject, run_time=run_time)
        self.animation_script = animation_script
        self.scene = scene

        self.pending_queue = collections.deque()
        for method_info in animation_script.entries:
            method = getattr(self.scene, method_info["name"])
            method.__func__.start_alpha = value_from_range_to_range(
                value=method_info["start_time"],
                init_min=0,
                init_max=self.run_time,
                new_min=0,
                new_max=1,
            )
            self.pending_queue.append(method)

        self.animation_pool = AnimationPool(mobject=self.mobject, scene=self.scene, total_run_time=self.run_time)

    def begin(self) -> None:
        """Override and do nothing to avoid ``interpolate_mobject`` being called twice with alpha equal to 0."""

    def interpolate_mobject(self, alpha: float) -> None:
        while self.pending_queue and self.pending_queue[0].start_alpha < 0:
            method = self.pending_queue.popleft()
            self.animation_pool.add(method)
            if len(self.pending_queue) >= 1:
                self.animation_pool.interpolate(self.pending_queue[0].start_alpha)
            else:
                raise NotImplementedError("Likely just have to ``self.animation_pool.interpolate(1)``")

        self.animation_pool.interpolate_finished_animations(alpha)

        if len(self.pending_queue) > 0 and alpha >= self.pending_queue[0].start_alpha:
            self.animation_pool.add(self.pending_queue.popleft())

        self.animation_pool.interpolate(alpha)


class AnimationPool:
    def __init__(self, mobject, scene, total_run_time: float) -> None:
        self.mobject = mobject
        self.scene = scene
        self.total_run_time = total_run_time
        self.animations: set[Animation] = set()
        self.queue = []
        self.backlog = []

    def add(self, method: Callable[[], Animation | Iterable[Animation]]) -> None:
        animations = method()
        if not isinstance(animations, Iterable):
            animations = [animations]

        for anim in animations:
            if anim is None:
                continue

            anim = prepare_animation(anim)
            anim.start_alpha = method.start_alpha

            anim.end_alpha = method.start_alpha + value_from_range_to_range(
                value=anim.run_time,
                init_min=0,
                init_max=self.total_run_time,
                new_min=0,
                new_max=1,
            )

            animations_with_timings = self._extract_animations_with_absolute_timings(anim)

            for animation, start_time, end_time in animations_with_timings:
                animation.start_alpha = anim.start_alpha + value_from_range_to_range(
                    value=start_time,
                    init_min=0,
                    init_max=self.total_run_time,
                    new_min=0,
                    new_max=1,
                )

                animation.end_alpha = anim.start_alpha + value_from_range_to_range(
                    value=end_time,
                    init_min=0,
                    init_max=self.total_run_time,
                    new_min=0,
                    new_max=1,
                )

                self._add_to_backlog(animation)

    def _add_to_backlog(self, new_animation: Animation) -> None:
        for index, anim in enumerate(self.backlog.copy()):
            if new_animation.start_alpha >= anim.start_alpha:
                self.backlog.insert(index, new_animation)
                break
        else:
            self.backlog.append(new_animation)

    def _extract_animations_with_absolute_timings(
        self,
        animation: Animation,
    ) -> Sequence[tuple[Animation, float, float]]:
        """Get animations with their absolute timings.

        The output is similar to ``AnimationGroup.anims_with_timings`` except
        that the timings are all relative to the overall animation, rather than
        an animation's immediate parent. For example, here's an animation and what the
        output would look like from this method:

        Input:
            animation = Succession(
                Succession(
                    FadeIn(Circle()),
                    FadeIn(Square()),
                ),
                AnimationGroup(
                    FadeIn(Circle()),
                    FadeIn(Square()),
                    FadeIn(Circle()),
                ),
                Succession(
                    Succession(
                        FadeIn(Circle()),
                        FadeIn(Square()),
                    ),
                    AnimationGroup(
                        FadeIn(Circle()),
                        Succession(
                            FadeIn(Rectangle()),
                            FadeIn(Ellipse()),
                        ),
                        FadeIn(Square()),
                    ),
                ),
            )

        Output:
            [(FadeIn(Circle), 0, 1.0),
             (FadeIn(Square), 1.0, 2.0),
             (FadeIn(Circle), 2.0, 3.0),
             (FadeIn(Square), 2.0, 3.0),
             (FadeIn(Circle), 2.0, 3.0),
             (FadeIn(Circle), 3.0, 4.0),
             (FadeIn(Square), 4.0, 5.0),
             (FadeIn(Circle), 5.0, 6.0),
             (FadeIn(Rectangle), 5.0, 6.0),
             (FadeIn(Ellipse), 6.0, 7.0),
             (FadeIn(Square), 5.0, 6.0)]

        Args:
            animation: The animation from which the timings will be extracted

        Returns:
            A list of tuple containing the animation, absolute start time, absolute end time
        """
        return list(
            self._extract_animations_with_absolute_timings_helper(
                animation,
                parent_start_time=0,
            ),
        )

    def _extract_animations_with_absolute_timings_helper(self, animation: Animation, parent_start_time: float):
        if not isinstance(animation, CuratorAnimationGroup):
            yield animation, 0, animation.run_time
        else:
            animations_with_timings = animation.anims_with_timings
            for subanimation, sub_start_time, sub_end_time in animations_with_timings:
                if not isinstance(subanimation, CuratorAnimationGroup):
                    yield subanimation, sub_start_time + parent_start_time, sub_end_time + parent_start_time
                else:
                    extracted_timings = self._extract_animations_with_absolute_timings_helper(
                        subanimation,
                        parent_start_time=sub_start_time,
                    )

                    subanimations_with_absolute_timings = []
                    for extracted_subanimation, extracted_start_time, extracted_end_time in extracted_timings:
                        subanimations_with_absolute_timings.append(
                            (
                                extracted_subanimation,
                                extracted_start_time + parent_start_time,
                                extracted_end_time + parent_start_time,
                            ),
                        )

                    yield from subanimations_with_absolute_timings

    def interpolate_finished_animations(self, alpha: float) -> None:
        for anim in self.animations.copy():
            if alpha >= anim.end_alpha:
                anim.finish()
                anim.clean_up_from_scene(self.scene)
                self.animations.remove(anim)

    def interpolate(self, alpha: float) -> None:
        for anim in self.backlog.copy():
            if anim.start_alpha <= alpha:
                self.backlog.remove(anim)
                self.animations.add(anim)
                anim._setup_scene(self.scene)
                anim.begin()

        for anim in self.animations.copy():
            if alpha < anim.end_alpha:
                anim.interpolate(
                    value_from_range_to_range(
                        value=alpha,
                        init_min=anim.start_alpha,
                        init_max=anim.end_alpha,
                        new_min=0,
                        new_max=1,
                    ),
                )
            else:
                anim.interpolate(1)
                anim.finish()
                anim.clean_up_from_scene(self.scene)
                self.animations.remove(anim)
