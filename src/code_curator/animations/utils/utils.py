from __future__ import annotations

import functools
import inspect
from functools import cached_property
from typing import TYPE_CHECKING

from manim.mobject.mobject import _AnimationBuilder
from manim import Animation
from manim import AnimationGroup
from manim import FadeIn
from manim import FadeOut
from manim import Mobject
from manim import Wait

from code_curator.animations.curator_animation import CuratorAnimation
from code_curator.animations.fixed_succession import FixedSuccession


if TYPE_CHECKING:
    from types import MethodType
    from code_curator.animations.animation_generator import AnimationGenerator

OVERRIDING_START_RUN_TIME_IN_SECONDS = 0.5
OVERRIDING_END_RUN_TIME_IN_SECONDS = 0.5

_IS_OVERRIDING_ANIMATION_ATTR_NAME = "is_overriding_animation"


def pre_scene_render_hook(first_scene_gen_method):
    curr_gen_method = first_scene_gen_method
    while curr_gen_method is not None:
        if _is_overriding_start(curr_gen_method.next):
            curr_gen_method.__func__.audio_duration -= OVERRIDING_START_RUN_TIME_IN_SECONDS

        if _is_overriding_end(curr_gen_method):
            curr_gen_method.__func__.audio_duration -= OVERRIDING_END_RUN_TIME_IN_SECONDS

        curr_gen_method = curr_gen_method.next


def decorator_wrapper(cls):
    class OverridingAnimationDeco:

        def __init__(self, *args, **kwargs) -> None:
            self.instance = cls(*args, **kwargs)
            self.first_gen_method = self.instance._get_first_gen_method()
            self.last_gen_method = self.instance._get_last_gen_method()

            label_as_overriding_start(self.first_gen_method)
            label_as_overriding_end(self.last_gen_method)

            if _is_transition_overriding_start(self.first_gen_method):
                self._remove_from_normal_animation_flow(self.first_gen_method)

        def __getattr__(self, item):
            return getattr(self.instance, item)

        @property
        def default_transition_animation(self):
            animation = Animation(mobject=Mobject(), run_time=0.0)
            # animation.remaining_time_for_transition = 0.0
            return animation

        def _remove_from_normal_animation_flow(self, gen_method) -> None:
            self.instance.sub_generators.remove(gen_method)
            del self.instance.animation_name_timing_map[gen_method.name]

    def _new_send(self, value=None):
        mobjects_on_screen_before_animation = self.mobjects.copy()
        transition_start_animation = self.default_transition_animation
        transition_start_animation.remaining_time = 0.0
        for attr in self.first_gen_method.__globals__.values():
            add_timing_validation(attr, self)

        if _is_transition_overriding_start(self.first_gen_method):
            # NOTE: Because we've removed this transition gen method from self.sub_generators
            # the code for setting the current func_name is never called so we have to do it ourselves
            self.func_name = self.first_gen_method.name
            transition_start_animation = next(self.first_gen_method())


        wait_time_post_transition_start_animation = transition_start_animation.remaining_time

        remove_timing_validation(FadeOut)
        self.play(
            FadeOut(*self.mobjects, run_time=OVERRIDING_START_RUN_TIME_IN_SECONDS),
            transition_start_animation,
        )

        remove_timing_validation(Wait)
        self.play(Wait(wait_time_post_transition_start_animation))
        add_timing_validation(Wait, self)

        add_timing_validation(FadeOut, self)
        last_animation = yield from self._get_sub_generators()

        remove_timing_validation(FadeOut)
        remove_timing_validation(FadeIn)

        self.play(
            AnimationGroup(
                FadeOut(*self.mobjects),
                FadeIn(*mobjects_on_screen_before_animation),
                run_time=OVERRIDING_END_RUN_TIME_IN_SECONDS,
            ),
        )

        add_timing_validation(FadeOut, self)
        add_timing_validation(FadeIn, self)

    OverridingAnimationDeco.send = _new_send

    OverridingAnimationDeco.__name__ = cls.__name__

    return OverridingAnimationDeco


def overriding_animation(obj):
    if inspect.isclass(obj):
        return decorator_wrapper(obj)

    fn = obj

    @functools.wraps(fn)
    def inner(self, *args, **kwargs):
        mobjects_on_screen_before_animation = self.mobjects.copy()
        remove_timing_validation(FadeOut)
        self.play(
            FadeOut(*self.mobjects, run_time=OVERRIDING_START_RUN_TIME_IN_SECONDS),
        )

        add_timing_validation(FadeOut, self)
        # TODO: Warn user somehow to only have one yield per generator method
        yield from fn(self, *args, **kwargs)

        remove_timing_validation(FadeOut)
        remove_timing_validation(FadeIn)

        self.play(
            AnimationGroup(
                FadeOut(*self.mobjects),
                FadeIn(*mobjects_on_screen_before_animation),
                run_time=OVERRIDING_END_RUN_TIME_IN_SECONDS,
            ),
        )

        add_timing_validation(FadeOut, self)
        add_timing_validation(FadeIn, self)

    inner.is_overriding_start = True
    inner.is_overriding_end = True
    inner.__globals__.update(fn.__globals__)

    return inner


TRANSITION_OVERRIDE_START_ATTR_NAME = 'transition_overriding_start'


def transition_overriding_start(fn) -> None:
    setattr(fn, TRANSITION_OVERRIDE_START_ATTR_NAME, True)
    return fn


def _is_transition_overriding_start(gen_method) -> bool:
    return hasattr(gen_method, TRANSITION_OVERRIDE_START_ATTR_NAME)



def is_overriding_animation(fn) -> bool:
    # AnimationGenerator instances will automatically delegate attribute look
    # up to owner's if using hasattr, which can lead to incorrect results. For
    # example, say we have a class outer and a nested class inner and outer is
    # overriding. A search for inner being overriding with hasattr will be
    # delegated up to outer and result in True, even though inner isn't
    # actually overriding.
    return _IS_OVERRIDING_ANIMATION_ATTR_NAME in fn.__class__.__dict__


def label_as_overriding_start(fn) -> None:
    if _is_transition_overriding_start(fn) and fn.audio_duration >= OVERRIDING_END_RUN_TIME_IN_SECONDS:
        return

    fn.__func__.is_overriding_start = True


def label_as_overriding_end(fn) -> None:
    fn.__func__.is_overriding_end = True


def _is_overriding_start(fn) -> bool:
    return hasattr(fn, "is_overriding_start")


def _is_overriding_end(fn) -> bool:
    return hasattr(fn, "is_overriding_end")


def add_timing_validation(animation_cls, animation_gen_owner):
    if (
        isinstance(animation_cls, type)
    and issubclass(animation_cls, Animation)
    and animation_cls is not Animation
    and animation_cls is not AnimationGroup
    and animation_cls is not FixedSuccession
    ):
        CuratorAnimation._owner = animation_gen_owner
        if CuratorAnimation not in animation_cls.__bases__:
            try:
                animation_cls.__bases__ = (CuratorAnimation,) + animation_cls.__bases__
            except TypeError:
                pass  # Can't add class to its own bases


def remove_timing_validation(animation_cls):
    # NOTE: Tentatively, ignoring this exception and proceeding without removing CuratorAnimation from Bases
    if CuratorAnimation is not animation_cls.__bases__[0]:
        return
        # raise RuntimeError(
        #     f"CuratorAnimation is not the first base in {animation_cls} but an attempt"
        #     " to remove it as such is being made",
        # )

    animation_cls.__bases__ = animation_cls.__bases__[1:]
