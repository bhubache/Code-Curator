from __future__ import annotations

from abc import ABC
from collections.abc import Sequence
from typing import TYPE_CHECKING

from manim import config
from manim import FadeOut
from manim import Mobject
from manim import Scene
from manim import Wait

from .generator_scene import GeneratorScene
from code_curator.animations.utils import utils
from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.animations.curator_animation_new import CuratorAnimation
from code_curator import constants
from code_curator.leetcode.scenes.present_problem.base_present_problem import BasePresentProblem
from code_curator.animations.curator_animation_new import ExcludeDuplicationSubmobjectsMobject


if TYPE_CHECKING:
    from .script_handling.components.animation_script.composite_animation_script import (  # noqa: E501
        CompositeAnimationScript,
    )

logger = CustomLogger.getLogger(__name__)


class MyClass:
    """Meant to simply hold attributes so one instance can be shared across streams."""


class _AllowOneMobjectList(list):
    def __setitem__(self, key, mobjects) -> None:
        raise NotImplementedError()
        # if len(mobjects) == 0 and isinstance(mobjects[0], ExcludeDuplicationSubmobjectsMobject):
        #     super().__setitem__(key, mobjects)

        # if len(mobjects) > 1:
        #     raise RuntimeError(f"{self.__class__.__name__}.mobjects should never exceed 1, it is currently {len(self.mobjects)}")

        # if len(mobjects) == 1 and not isinstance(mobjects[0], ExcludeDuplicationSubmobjectsMobject):
        #     raise RuntimeError(f"Only {ExcludeDuplicationSubmobjectsMobject.__name__} should be in {self.__class__.__name__}.mobjects, found {self.mobjects}")


class _AllowOneMobjectDescriptor:
    def __set_name__(self, owner, name: str) -> None:
        self.private_name = "_" + name

    def __get__(self, instance, owner=None):
        return getattr(instance, self.private_name)

    def __set__(self, instance, value) -> None:
        if not hasattr(instance, self.private_name):
            if len(value) != 1:
                return

            if not isinstance(value[0], ExcludeDuplicationSubmobjectsMobject):
                return

            setattr(instance, self.private_name, _AllowOneMobjectList(value[0]))


class BaseScene(Scene):
    config["background_color"] = constants.DEFAULT_BACKGROUND_COLOR
    config["disable_caching"] = True

    mobjects = _AllowOneMobjectDescriptor()

    def __init__(self, animation_script, stream_clses: list[type]) -> None:
        super().__init__()
        self.animation_script = animation_script
        self.stream_instances = []
        self._setup_attrs(stream_clses)

    # @property
    # def mobjects(self) -> Sequence[Mobject]:
    #     if ExcludeDuplicationSubmobjectsMobject() in self._mobjects:
    #         raise BaseException()

    #     return self._mobjects

    # @mobjects.setter
    # def mobjects(self, value: Sequence[Mobject]) -> None:
    #     self._mobjects = value

    # def __instantiate_streams(self, stream_clses: list[type]) -> None:
    #     attrs_before_scene_init

    def _setup_attrs(self, stream_clses: list[type]) -> None:
        attrs_before_attr_setup = set(self.__dict__.keys())
        self.initialize_scene()
        newly_added_attrs = set(self.__dict__.keys()) - attrs_before_attr_setup

        # for stream_inst in self.stream_instances:
        #     for attr_name in newly_added_attrs:
        #         setattr(stream_inst, attr_name, getattr(self, attr_name))

        dict_to_pass = {attr_name: getattr(self, attr_name) for attr_name in newly_added_attrs}

        shared_instance = MyClass()

        for stream_cls in stream_clses:
            self.stream_instances.append(stream_cls(**dict_to_pass, scene=self, shared=shared_instance))

    def setup_attrs(self) -> None:
        pass

    def construct(self) -> None:
        self.play(
            CuratorAnimation(
                self.animation_script._animation_script,
                stream_instances=self.stream_instances,
                run_time=self.animation_script.run_time,
                scene=self,
            )
        )

    @property
    def scene_mobjects(self) -> list[Mobject]:
        return self.mobjects[0].submobjects

    # def add(self, *mobjects: Mobject) -> None:
    #     if len(mobjects) == 0 and isinstance(mobjects[0], ExcludeDuplicationSubmobjectsMobject):
    #         super().add(mobjects[0])

    #     if len(mobjects) > 1:
    #         raise RuntimeError(f"{self.__class__.__name__}.mobjects should never exceed 1, it is currently {len(self.mobjects)}")

    #     if len(mobjects) == 1 and not isinstance(mobjects[0], ExcludeDuplicationSubmobjectsMobject):
    #         raise RuntimeError(f"Only {ExcludeDuplicationSubmobjectsMobject.__name__} should be in {self.__class__.__name__}.mobjects, found {self.mobjects}")



# class BaseScene(ABC, GeneratorScene):
#     config.background_color = "#000E15"
#     generator_classes = []
#
#     def __init__(
#         self,
#         problem_dir: str,
#         aligned_animation_scene: CompositeAnimationScript,
#         *args,
#         **kwargs,
#     ) -> None:
#         super().__init__(
#             *args,
#             aligned_animation_script=aligned_animation_scene,
#             **kwargs,
#         )
#         self._aligned_animation_scene: CompositeAnimationScript = (
#             aligned_animation_scene
#         )
#         self._problem_dir: str = problem_dir
#
#     @property
#     def aligned_animation_scene(self) -> CompositeAnimationScript:
#         return self._aligned_animation_scene
#
#     @property
#     def problem_dir(self) -> str:
#         return self._problem_dir
#
#     def render(self, preview: bool = False):
#         self.prep_rendering()
#         super().render()
#
#     def prep_rendering(self):
#         super().prep_rendering()
#         self._make_doubly_linked_generators(
#             self.sub_generators,
#             self.aligned_animation_scene,
#         )
#         utils.pre_scene_render_hook(self.golden_flattened_generators[0])
#
#
#     def construct(self) -> None:
#         animation_generator = next(self)
#         for i, animation in enumerate(animation_generator):
#             logger.critical(f"{i}   {animation}")
#             self.play(animation)
#
#             wait_animation = self.__create_filling_wait_animation(animation)
#             if wait_animation is not None:
#                 self.play(wait_animation)
#
#     def tear_down(self) -> None:
#         self.play(FadeOut(*self.mobjects))
#
#     # TODO: Move this to somewhere internal
#     def __create_filling_wait_animation(self, animation) -> Wait:
#         # Remove CuratorAnimation from bases to create basic manim Wait
#         utils.remove_timing_validation(Wait)
#
#         try:
#             if animation.remaining_time > 0:
#                 return Wait(animation.remaining_time)
#         except AttributeError:
#             min_remaining_time = float("inf")
#             try:
#                 for sub_anim in animation.animations:
#                     try:
#                         min_remaining_time = min(
#                             sub_anim.remaining_time,
#                             min_remaining_time,
#                         )
#                     except AttributeError:
#                         min_remaining_time = 1.0
#             except AttributeError:
#                 min_remaining_time = 1.0
#
#             return Wait(min_remaining_time)
#
#     def _make_doubly_linked_generators(self, sub_generators, aligned_animation_helper):
#         for i, generator_method in enumerate(self.golden_flattened_generators):
#             generator_method.__func__.prev = self.golden_flattened_generators[i - 1]
#             try:
#                 generator_method.__func__.next = self.golden_flattened_generators[i + 1]
#             except IndexError:
#                 generator_method.__func__.next = None  # last gen method
#
#         # Break cycle between first and last generator methods
#         self.golden_flattened_generators[0].__func__.prev = None
