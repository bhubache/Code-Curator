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
        while self.pending_queue[0].start_alpha < 0:
            method = self.pending_queue.popleft()
            self.animation_pool.add(method)
            for animation in self.animation_pool.animations.copy():
                animation.interpolate(1)
                animation.finish()
                animation.clean_up_from_scene(self.scene)
                self.animation_pool.animations.remove(animation)

    def interpolate_mobject(self, alpha: float) -> None:
        if len(self.pending_queue) > 0 and alpha >= self.pending_queue[0].start_alpha:
            self.animation_pool.add(self.pending_queue.popleft())

        self.animation_pool.interpolate(alpha)


class AnimationPool:
    def __init__(self, mobject, scene, total_run_time: float) -> None:
        self.mobject = mobject
        self.scene = scene
        self.total_run_time = total_run_time
        self.animations: set[Animation] = set()

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
            self.animations.add(anim)
            anim._setup_scene(self.scene)
            anim.begin()

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
