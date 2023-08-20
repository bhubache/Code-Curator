from __future__ import annotations

import inspect
from collections.abc import Generator
from collections.abc import Sequence
from typing import TYPE_CHECKING

from manim import Animation
from manim import AnimationGroup
from manim import Wait

from code_curator.animations.curator_animation import CuratorAnimation
from code_curator.animations.fixed_succession import FixedSuccession
from code_curator.auto_animation_timer import AutoAnimationTimer
from code_curator.custom_logging.custom_logger import CustomLogger


logger = CustomLogger.getLogger(__name__)


if TYPE_CHECKING:
    from types import TracebackType
    from code_curator.base_scene import BaseScene


class AnimationGenerator(Generator):
    def __init__(
        self,
        *args,
        owner: BaseScene | None,
        aligned_animation_script,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.owner = owner
        self.aligned_animation_script = aligned_animation_script
        self.animation_name_timing_map = {
            child.unique_id: child.audio_duration
            for child in self.aligned_animation_script.children
        }
        self.sub_generators: Sequence[Generator] = []
        self._post_init()

    def __getattr__(self, item: str):
        owner = self.owner
        while True:
            try:
                return getattr(owner, item)
            except AttributeError:
                try:
                    owner = owner.owner
                except AttributeError:
                    print(f"Unable to find item {item}!")
                    breakpoint()
                    raise

    def _post_init(self) -> None:
        """Construct your class."""

    def prep_rendering(self):
        self.sub_generators = self._get_organized_sub_generators()

    def send(self, value=None):
        return self._get_sub_generators()

    def throw(
        self,
        type_: type[BaseException],
        val: BaseException | object = ...,
        tb: TracebackType | None = ...,
    ):
        pass

    @staticmethod
    def _is_generator_function(obj) -> bool:
        return inspect.isgeneratorfunction(obj)

    def _get_organized_sub_generators(self):
        animation_gens = []
        for animation_name in self.animation_name_timing_map:
            # TODO: Default animation names starting with an underscore as Wait
            if animation_name.startswith("_"):

                def _wait(self):
                    yield Wait()

                _wait.__name__ = animation_name

                setattr(self.__class__, animation_name, _wait)

            animation_gens.append(getattr(self, animation_name))

        return animation_gens

    def _is_generator(self, obj) -> bool:
        return self._is_generator_function(obj) or issubclass(obj, Generator)

    def _get_sub_generators(self):
        for gen_method in self.sub_generators:
            if self._is_generator_function(gen_method):
                gen_method = AutoAnimationTimer.time(
                    gen_method,
                    owner=self,
                )
                self._insert_timing_logic(gen_method)
                yield from gen_method(self)
            else:
                cls_gen = gen_method(
                    owner=self,
                    aligned_animation_script=self.aligned_animation_script.get_child(
                        gen_method.__name__,
                    ),
                )
                cls_gen.prep_rendering()
                yield from cls_gen.send(None)

    # TODO: _MethodAnimation
    def _insert_timing_logic(self, gen_method):
        for attr_value in gen_method.__globals__.values():
            if (
                isinstance(attr_value, type)
                and issubclass(attr_value, Animation)
                and attr_value is not Animation
                and attr_value is not AnimationGroup
                and attr_value is not FixedSuccession
            ):
                CuratorAnimation._owner = self
                if CuratorAnimation not in attr_value.__bases__:
                    try:
                        attr_value.__bases__ = (
                            CuratorAnimation,
                        ) + attr_value.__bases__
                    except TypeError:
                        pass  # Can't add class to its own bases

    def _get_gen_name(self, obj) -> str:
        return obj.__name__
