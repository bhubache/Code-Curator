from __future__ import annotations

import inspect
from collections.abc import Generator
from collections.abc import Sequence
from typing import TYPE_CHECKING

from manim import Wait

from code_curator.animations.utils import utils
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
        # self._adjust_timing_for_overriding_animations()

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

    def _adjust_timing_for_overriding_animations(self) -> None:
        breakpoint()
        for i, gen_method in enumerate(self.sub_generators):
            if utils.is_overriding_animation(gen_method):
                self._adjust_timing_for_overriding_start(i)
                self._adjust_timing_for_overriding_end(i)

    def _get_cls_attributes_in_order(self, cls):
        if not inspect.isclass(cls):
            raise TypeError(f"Expected class, got {type(cls)}")

        return list(cls.__dict__)

    def _adjust_timing_for_overriding_start(self, overriding_gen_method_index):
        breakpoint()
        previous_gen_obj = self.sub_generators[overriding_gen_method_index - 1]
        if inspect.isclass(previous_gen_obj):
            previous_gen_obj = self._get_latest_gen_method(previous_gen_obj)

        breakpoint()
        prev_gen_method = self.sub_generators[overriding_gen_method_index - 1]
        self.animation_name_timing_map[
            prev_gen_method.__name__
        ] -= utils.OVERRIDING_START_RUN_TIME_IN_SECONDS

    def _get_latest_gen_method(self, gen_method):
        for attr_name in reversed(self._get_cls_attributes_in_order(gen_method)):
            attr_value = getattr(gen_method, attr_name)
            if self._is_generator_function(attr_value):
                return attr_value

            if self._is_generator(attr_value):
                return self._get_latest_gen_method(attr_value)

    def _adjust_timing_for_overriding_end(self, overriding_gen_method_index):
        next_gen_method = self.sub_generators[overriding_gen_method_index + 1]
        self.animation_name_timing_map[
            next_gen_method.__name__
        ] -= utils.OVERRIDING_END_RUN_TIME_IN_SECONDS

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
            utils.add_timing_validation(attr_value, self)

    def _get_gen_name(self, obj) -> str:
        return obj.__name__
