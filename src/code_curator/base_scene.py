from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from manim import config
from manim import FadeOut
from manim import Wait

from .generator_scene import GeneratorScene
from code_curator.animations.utils import utils
from code_curator.custom_logging.custom_logger import CustomLogger


if TYPE_CHECKING:
    from .script_handling.components.animation_script.composite_animation_script import (  # noqa: E501
        CompositeAnimationScript,
    )

logger = CustomLogger.getLogger(__name__)


class BaseScene(ABC, GeneratorScene):
    config.background_color = "#000E15"
    generator_classes = []

    def __init__(
        self,
        problem_dir: str,
        aligned_animation_scene: CompositeAnimationScript,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            *args,
            aligned_animation_script=aligned_animation_scene,
            **kwargs,
        )
        self._aligned_animation_scene: CompositeAnimationScript = (
            aligned_animation_scene
        )
        self._problem_dir: str = problem_dir

    @property
    def aligned_animation_scene(self) -> CompositeAnimationScript:
        return self._aligned_animation_scene

    @property
    def problem_dir(self) -> str:
        return self._problem_dir

    def render(self, preview: bool = False):
        self.prep_rendering()
        super().render()

    def prep_rendering(self):
        super().prep_rendering()
        self._make_doubly_linked_generators(
            self.sub_generators,
            self.aligned_animation_scene,
        )

    def construct(self) -> None:
        animation_generator = next(self)
        for i, animation in enumerate(animation_generator):
            logger.critical(f"{i}   {animation}")
            self.play(animation)

            wait_animation = self.__create_filling_wait_animation(animation)
            if wait_animation is not None:
                self.play(wait_animation)

    def tear_down(self) -> None:
        self.play(FadeOut(*self.mobjects))

    # TODO: Move this to somewhere internal
    def __create_filling_wait_animation(self, animation) -> Wait:
        # Remove CuratorAnimation from bases to create basic manim Wait
        utils.remove_timing_validation(Wait)

        try:
            if animation.remaining_time > 0:
                return Wait(animation.remaining_time)
        except AttributeError:
            min_remaining_time = float("inf")
            try:
                for sub_anim in animation.animations:
                    try:
                        min_remaining_time = min(
                            sub_anim.remaining_time,
                            min_remaining_time,
                        )
                    except AttributeError:
                        min_remaining_time = 1.0
            except AttributeError:
                min_remaining_time = 1.0

            return Wait(min_remaining_time)

    def _make_doubly_linked_generators(self, sub_generators, aligned_animation_helper):
        for i, generator_method in enumerate(self.golden_flattened_generators):
            generator_method.__func__.prev = self.golden_flattened_generators[i - 1]
            try:
                generator_method.__func__.next = self.golden_flattened_generators[i + 1]
            except IndexError:
                generator_method.__func__.next = None  # last gen method

        # Break cycle between first and last generator methods
        self.golden_flattened_generators[0].__func__.prev = None
