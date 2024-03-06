from __future__ import annotations

import collections
from collections.abc import Iterable
from typing import Callable

from manim import Animation
from manim import prepare_animation

from .utils.math_ import value_from_range_to_range


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
            for animation in self.animation_pool.animations.copy():
                animation.interpolate(1)
                animation.finish()
                animation.clean_up_from_scene(self.scene)
                self.animation_pool.animations.remove(animation)

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

            breakpoint()
            animations_with_timings = self._extract_animations_with_timings(anim)

            for animation, start_time, end_time in animations_with_timings:
                animation.start_alpha = anim.start_alpha + value_from_range_to_range(
                    value=start_time,
                    init_min=0,
                    init_max=self.total_run_time,
                    new_min=0,
                    new_max=1,
                )

                animation.end_alpha = anim.start_alpha + value_from_range_to_value(
                    value=end_time,
                    init_min=0,
                    init_max=self.total_run_time,
                    new_min=0,
                    new_max=1,
                )

                self.backlog.append(animation)

            for a in self.backlog:
                if a.start_alpha == anim.start_alpha:
                    self.animations.add(anim)
                    anim._setup_scene(self.scene)
                    anim.begin()

    def _extract_animations_with_timings(self, animation: Animation):
        animations_with_timings = list(self._extract_animations_with_timings_helper(animation))

        # max_value = 0
        # for index, (anim, start_time, end_time) in enumerate(animations_with_timings.copy()):
        #     if start_time < max_value:
        #         start_time += max_value

        #     if end_time < max_value:
        #         end_time += max_value

        #     animations_with_timings[index] = (
        #         anim,
        #         start_time,
        #         end_time,
        #     )

        #     max_value = max(max_value, start_time, end_time)

        return animations_with_timings

    def _extract_animations_with_timings_helper(self, animation: Animation):
        try:
            animations_with_timings = animation.anims_with_timings
        except AttributeError:
            yield animation, 0, animation.run_time
        else:
            for anim, start_time, end_time in animations_with_timings:
                try:
                    anims_with_timings = anim.anims_with_timings
                except AttributeError:
                    yield anim, start_time, end_time
                else:
                    breakpoint()
                    inter = self._extract_animations_with_timings_helper(anim)
                    yield from inter

    # def _unpack_animation(self, animation: Animation, start_alpha: float) -> None:
    #     if not isinstance(animation, CuratorAnimationGroup):
    #         animation.start_alpha = start_alpha
    #         animation.end_alpha = start_alpha + value_from_range_to_range(
    #             value=animation.run_time,
    #             init_min=0,
    #             init_max=self.total_run_time,
    #             new_min=0,
    #             new_max=1,
    #         )

    #         yield animation
    #     else:
    #         offset = 0

    #         for index, anim in enumerate(animation.animations):
    #             if index > 0:
    #                 prev_run_time = animation.animations[index - 1].get_run_time()
    #                 offset += value_from_range_to_range(
    #                     value=prev_run_time * animation.lag_ratio,
    #                     init_min=0,
    #                     init_max=self.total_run_time,
    #                     new_min=0,
    #                     new_max=1,
    #                 )

    #             yield from self._unpack_animation(
    #                 anim,
    #                 start_alpha + offset
    #             )

    def interpolate_finished_animations(self, alpha: float) -> None:
        for anim in self.animations.copy():
            if alpha >= anim.end_alpha:
                anim.finish()
                anim.clean_up_from_scene(self.scene)
                self.animations.remove(anim)

    def interpolate(self, alpha: float) -> None:
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
                anim.finish()
                anim.clean_up_from_scene(self.scene)
                self.animations.remove(anim)
