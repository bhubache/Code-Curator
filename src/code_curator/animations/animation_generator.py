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
    from types import FunctionType
    from types import MethodType
    from code_curator.base_scene import BaseScene
    from ..script_handling.components.animation_script.composite_animation_script import (  # noqa: E501
        CompositeAnimationScript,
    )

    # NOTE: This could mess up with inserting CuratorAnimation into bases
    from manim import Animation


class AnimationGenerator(Generator):
    golden_flattened_generators = []

    def __init__(
        self,
        *args,
        aligned_animation_script: CompositeAnimationScript,
        owner: BaseScene | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.owner = owner
        self.aligned_animation_script = aligned_animation_script
        self.animation_name_timing_map: dict[str, float] = {
            child.unique_id: child.audio_duration
            for child in self.aligned_animation_script.children
        }
        self.sub_generators: Sequence[MethodType | AnimationGenerator] = (
            self._get_organized_sub_generators()
        )

    def __getattr__(self, attr_name: str):
        owner = self.owner
        while True:
            try:
                return getattr(owner, attr_name)
            except AttributeError:
                try:
                    owner = owner.owner
                except AttributeError:
                    print(f"Unable to find attr_name {attr_name}!")
                    raise

    def initialize(self) -> None:
        """Construct your class."""

    def prep_rendering(self) -> None:
        self.initialize()

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

    def _get_organized_sub_generators(
        self,
    ) -> Sequence[MethodType | AnimationGenerator]:
        animation_gens = []
        for animation_name in self.animation_name_timing_map:
            if animation_name.startswith("_"):

                def _wait(_):
                    yield Wait()

                _wait.__name__ = animation_name

                setattr(self.__class__, animation_name, _wait)

            animation_gens.append(getattr(self, animation_name))

        for i, gen in enumerate(animation_gens):
            if self._is_generator_function(gen):
                self.golden_flattened_generators.append(gen)
            else:
                animation_gens[i] = gen(
                    owner=self,
                    aligned_animation_script=self.aligned_animation_script.get_child(
                        gen.__name__,
                    ),
                )

        if utils.is_overriding_animation(self):
            utils.label_as_overriding_start(
                self.__get_first_gen_method(animation_gens),
            )
            utils.label_as_overriding_end(
                self.__get_last_gen_method(animation_gens),
            )

        return animation_gens

    def _is_generator(self, obj) -> bool:
        return self._is_generator_function(obj) or issubclass(obj, Generator)

    def _get_sub_generators(self) -> Generator[Animation, None, None]:
        for gen in self.sub_generators:
            if self._is_generator_function(gen):
                gen = AutoAnimationTimer.time(gen, owner=self)
                self._insert_timing_logic(gen)
                yield from gen(self)
            else:
                gen.prep_rendering()
                yield from gen.send(None)

    # TODO: _MethodAnimation
    def _insert_timing_logic(self, gen_method: MethodType | FunctionType) -> None:
        for attr_value in gen_method.__globals__.values():
            utils.add_timing_validation(attr_value, self)

    def _get_gen_name(self, obj) -> str:
        return obj.__name__

    def __get_extremity_gen_method(
        self,
        sub_generators: Sequence[MethodType | AnimationGenerator],
        index: int,
    ) -> MethodType:
        if self._is_generator_function(sub_generators[index]):
            return sub_generators[index]

        return sub_generators[index].__get_extremity_gen_method(
            sub_generators[index].sub_generators,
            index,
        )

    def __get_first_gen_method(
        self,
        sub_generators: Sequence[MethodType | AnimationGenerator],
    ) -> MethodType:
        return self.__get_extremity_gen_method(sub_generators=sub_generators, index=0)

    def __get_last_gen_method(
        self,
        sub_generators: Sequence[MethodType | AnimationGenerator],
    ) -> MethodType:
        return self.__get_extremity_gen_method(sub_generators=sub_generators, index=-1)
