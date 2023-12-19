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


class _MobjectSentinel(Mobject):
    def __new__(cls):
        if not hasattr(cls, "singleton_instance"):
            cls.instance = super().__new__(cls)

        return cls.instance


class ExcludeDuplicationSubmobjectsMobject(Mobject):
    def remove(self, *mobjects: Mobject) -> Mobject:
        # If more than one mobject has been passed to a single FadeOut animation,
        # all the mobjects will be wrapped in a Group. So, we need to iterate over
        # the group to remove each mobject.
        for mobject_to_remove in mobjects:
            if isinstance(mobject_to_remove, Group):
                for submobject_to_remove in mobject_to_remove:
                    self.remove(submobject_to_remove)

            self._remove(
                mobject_to_remove=mobject_to_remove,
                mobject_to_search=self,
                mobject_container=None,
            )

        self._remove_all_sentinels()

        return self

    def _remove(
        self,
        *,
        mobject_to_remove: Mobject,
        mobject_to_search: Mobject,
        mobject_container: Mobject | None,
    ) -> None:
        try:
            problem_tex_parent = mobject_to_search.problem_tex_parent
        except AttributeError:
            pass
        else:
            if mobject_to_remove is problem_tex_parent:
                self._place_sentinel(
                    mobject_container=mobject_container,
                    mobject_to_remove=mobject_to_search,
                )

        if mobject_to_remove in mobject_to_search.submobjects:
            self._place_sentinel(
                mobject_container=mobject_to_search,
                mobject_to_remove=mobject_to_remove,
            )

        # FIXME: I think some mobjects aren't being removed because we're modifying
        #   the length of mobject_to_search.submobjects while iterating?

        for mobject in mobject_to_search.submobjects:
            self._remove(
                mobject_to_remove=mobject_to_remove,
                mobject_to_search=mobject,
                mobject_container=mobject_to_search,
            )

    def _place_sentinel(
        self,
        *,
        mobject_container: Mobject,
        mobject_to_remove: Mobject,
    ) -> None:
        index: int = mobject_container.submobjects.index(mobject_to_remove)
        mobject_container.submobjects[index] = _MobjectSentinel()

    def _remove_all_sentinels(self) -> None:
        # TODO: Remove empty Groups?
        new_submobjects = []
        for submobject in self.submobjects:
            if isinstance(submobject, _MobjectSentinel):
                continue

            try:
                submobject.submobjects = self._remove_all_sentinels_helper(submobject)
            except AttributeError:
                pass
            finally:
                new_submobjects.append(submobject)

        self.submobjects = new_submobjects

    def _remove_all_sentinels_helper(self, mobject: Mobject):
        new_submobjects: list[Mobject] = []
        for submobject in mobject.submobjects:
            if isinstance(submobject, _MobjectSentinel):
                continue

            try:
                submobject.submobjects = self._remove_all_sentinels_helper(submobject)
            except AttributeError:
                pass
            finally:
                new_submobjects.append(submobject)

        return new_submobjects


class CuratorAnimation(Animation):
    def __init__(self, animation_script, scene, run_time: float) -> None:
        super().__init__(ExcludeDuplicationSubmobjectsMobject(), run_time=run_time, suspend_mobject_updating=True)
        self.animation_script = animation_script
        self.scene = scene

        # TODO: See if this is actually needed
        setattr(self.scene, "mobjects", [self.mobject])

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
