from __future__ import annotations

import functools
import inspect

from manim import Animation
from manim import AnimationGroup
from manim import FadeIn
from manim import FadeOut

from code_curator.animations.curator_animation import CuratorAnimation
from code_curator.animations.fixed_succession import FixedSuccession

OVERRIDING_START_RUN_TIME_IN_SECONDS = 0.5
OVERRIDING_END_RUN_TIME_IN_SECONDS = 0.5

_IS_OVERRIDING_ANIMATION_ATTR_NAME = "is_overriding_animation"


def overriding_animation(obj):
    setattr(obj, _IS_OVERRIDING_ANIMATION_ATTR_NAME, True)

    if inspect.isclass(obj):
        return obj

    fn = obj

    @functools.wraps(fn)
    def inner(self, *args, **kwargs):
        mobjects_on_screen_before_animation = self.mobjects.copy()
        remove_timing_validation(FadeOut)
        self.play(
            FadeOut(*self.mobjects, run_time=OVERRIDING_START_RUN_TIME_IN_SECONDS),
        )

        add_timing_validation(FadeOut, self)
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

    inner.__globals__.update(fn.__globals__)

    return inner


def is_overriding_animation(fn) -> bool:
    return hasattr(fn, _IS_OVERRIDING_ANIMATION_ATTR_NAME)


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
    if CuratorAnimation is not animation_cls.__bases__[0]:
        raise RuntimeError(
            f"CuratorAnimation is not the first base in {animation_cls} but an attempt"
            " to remove it as such is being made",
        )

    animation_cls.__bases__ = animation_cls.__bases__[1:]
