from __future__ import annotations

import functools
import inspect
from typing import TYPE_CHECKING

from manim import Animation
from manim import AnimationGroup
from manim import FadeIn
from manim import FadeOut

from code_curator.animations.curator_animation import CuratorAnimation
from code_curator.animations.fixed_succession import FixedSuccession


if TYPE_CHECKING:
    from types import MethodType
    from code_curator.animations.animation_generator import AnimationGenerator

OVERRIDING_START_RUN_TIME_IN_SECONDS = 0.5
OVERRIDING_END_RUN_TIME_IN_SECONDS = 0.5

_IS_OVERRIDING_ANIMATION_ATTR_NAME = "is_overriding_animation"


def overriding_animation(
    obj: MethodType | type[AnimationGenerator],
) -> MethodType | type[AnimationGenerator]:
    """Return class/method decorator for enabling overriding animation(s).

    Args:
        obj: Object which will yield one or more overriding animations.
    """
    if inspect.isclass(obj):
        setattr(obj, _IS_OVERRIDING_ANIMATION_ATTR_NAME, True)

        def _new_send(self, value=None):
            mobjects_on_screen_before_animation = self.mobjects.copy()
            self.play(
                FadeOut(*self.mobjects, run_time=OVERRIDING_START_RUN_TIME_IN_SECONDS),
            )

            add_timing_validation(FadeOut, self)
            yield from self._get_sub_generators()

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

        obj.send = _new_send
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
        # TODO: Warn user somehow to only have one yield per generator method
        yield fn(self, *args, **kwargs)

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


def is_overriding_animation(fn) -> bool:
    # AnimationGenerator instances will automatically delegate attribute look
    # up to owner's if using hasattr, which can lead to incorrect results. For
    # example, say we have a class outer and a nested class inner and outer is
    # overriding. A search for inner being overriding with hasattr will be
    # delegated up to outer and result in True, even though inner isn't
    # actually overriding.
    return _IS_OVERRIDING_ANIMATION_ATTR_NAME in fn.__class__.__dict__


def label_as_overriding_start(fn) -> None:
    fn.__func__.is_overriding_start = True


def label_as_overriding_end(fn) -> None:
    fn.__func__.is_overriding_end = True


def is_overriding_start(fn) -> bool:
    return hasattr(fn, "is_overriding_start")


def is_overriding_end(fn) -> bool:
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
    if CuratorAnimation is not animation_cls.__bases__[0]:
        raise RuntimeError(
            f"CuratorAnimation is not the first base in {animation_cls} but an attempt"
            " to remove it as such is being made",
        )

    animation_cls.__bases__ = animation_cls.__bases__[1:]
