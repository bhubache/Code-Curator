from __future__ import annotations

import collections
from collections.abc import Iterable
from collections.abc import Sequence
from typing import Callable

from manim import Animation
from manim import Group
from manim import Mobject
from manim import prepare_animation

from .utils.math_ import value_from_range_to_range


# NOTE: I believe a mobject must be added to Animation.mobject for it to be animated!!!

# TODO: REFACTOR!
# TODO: Overriding animations
# TODO: Consider using a frame counter rather than mapping alpha to self.alphas element
# TODO: DO prepare_animation before animation start?!




class CuratorAnimation(Animation):
    def __init__(self, mobject, animation_script, scene, run_time: float) -> None:
        super().__init__(mobject, run_time=run_time, suspend_mobject_updating=True)
        self.animation_script = animation_script
        self.scene = scene

        # TODO: See if this is actually needed
        # setattr(self.scene, "mobjects", [self.mobject])

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
            anim = prepare_animation(anim)
            anim.start_alpha = method.start_alpha
            anim.end_alpha = method.start_alpha + value_from_range_to_range(
                value=anim.run_time,
                init_min=0,
                init_max=self.total_run_time,
                new_min=0,
                new_max=1,
            )
            self.mobject.add(anim.mobject)
            self.animations.add(anim)
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
                anim.clean_up_from_scene(self.scene)
                self.mobject.remove(
                    *self._get_remover_animation_mobjects(anim),
                )
                self.mobject.add(
                    *self._get_introducer_animation_mobjects(anim),
                )
                self.animations.remove(anim)

    def _get_remover_animation_mobjects(self, animation: Animation) -> Sequence[Mobject]:
        mobjects_to_be_removed: list[Mobject] = []
        if animation.is_remover():
            mobjects_to_be_removed.append(animation.mobject)
        else:
            try:
                child_animations = animation.animations
            except AttributeError:
                pass
            else:
                for child_anim in child_animations:
                    mobjects_to_be_removed.extend(
                        self._get_remover_animation_mobjects(child_anim),
                    )

        return mobjects_to_be_removed

    def _get_introducer_animation_mobjects(self, animation: Animation) -> Sequence[Mobject]:
        mobjects_to_be_introduced: list[Mobject] = []
        if animation.is_introducer():
            mobjects_to_be_introduced.append(animation.mobject)
        else:
            try:
                child_animations = animation.animations
            except AttributeError:
                pass
            else:
                for child_anim in child_animations:
                    mobjects_to_be_introduced.extend(
                        self._get_introducer_animation_mobjects(child_anim),
                    )

        return mobjects_to_be_introduced
