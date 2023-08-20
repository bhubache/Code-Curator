from __future__ import annotations

import inspect
from abc import ABC
from collections.abc import Callable
from collections.abc import Iterable
from typing import TYPE_CHECKING

from manim import config
from manim import FadeIn
from manim import FadeOut
from manim import Wait

from .generator_scene import GeneratorScene
from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.scene_scheduler import SceneScheduler


if TYPE_CHECKING:
    from .script_handling.components.animation_script.composite_animation_script import (  # noqa: E501
        CompositeAnimationScript,
    )

logger = CustomLogger.getLogger(__name__)


class BaseScene(ABC, GeneratorScene):
    config.background_color = "#000E15"

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
        self._animation_spec: dict = {}
        self._scene_scheduler: SceneScheduler = SceneScheduler()
        self._mobjects_pickle: str = "mobjects_pickle.pkl"

    def __getattr__(self, attr_name):
        section_name = inspect.stack()[1].function
        subsection_name = "_".join(attr_name.split("_")[:-1])
        subsection_number = attr_name.split("_")[-1]
        if subsection_number.isnumeric():
            component_name = f"{section_name}_{subsection_number}"
            timing_info_name = subsection_name
        else:
            component_name = section_name
            timing_info_name = section_name

        animation_leaf = self.aligned_animation_scene.get_component_deprecated(
            component_name,
        )
        try:
            timing_info = getattr(
                animation_leaf,
                animation_leaf.SUBANIMATION_TIMINGS_NAME,
            )
        except AttributeError as attr_exc:
            raise NotImplementedError(attr_name) from attr_exc

        return timing_info[timing_info_name].copy()

    @property
    def aligned_animation_scene(self) -> CompositeAnimationScript:
        return self._aligned_animation_scene

    @property
    def problem_dir(self) -> str:
        return self._problem_dir

    @property
    def animation_spec(self) -> dict:
        return self._animation_spec

    @property
    def scene_scheduler(self) -> SceneScheduler:
        return self._scene_scheduler

    def render(self, preview: bool = False):
        self.prep_rendering()
        super().render()

    def construct(self) -> None:
        animation_generator = next(self)
        for i, animation in enumerate(animation_generator):
            logger.critical(f"{i}   {animation}")
            # if i < 6 or i == 20:
            self.play(animation)

            wait_animation = self.__create_filling_wait_animation(animation)
            if wait_animation is not None:
                self.play(wait_animation)

    def __create_filling_wait_animation(self, animation) -> Wait:
        assert len(Wait.__bases__) == 2
        # Remove CuratorAnimation from bases to create basic manim Wait
        Wait.__bases__ = Wait.__bases__[1:]
        try:
            if animation.remaining_time > 0:
                return Wait(animation.remaining_time)
        except AttributeError:
            min_remaining_time = float("inf")
            try:
                for sub_anim in animation.animations:
                    try:
                        min_remaining_time = min(
                            sub_anim.remaining_time, min_remaining_time
                        )
                    except AttributeError:
                        min_remaining_time = 1.0
            except AttributeError:
                min_remaining_time = 1.0

            return Wait(min_remaining_time)

    def tear_down(self) -> None:
        self.play(FadeOut(*self.mobjects))

    def super_add_overriding_animation(
        self,
        composite: CompositeAnimationScript,
    ) -> Callable:
        def inner() -> None:
            mobjects_on_screen_before_animation = self.mobjects.copy()

            self.play(
                FadeOut(*self.mobjects),
                run_time=composite.override_start_time,
            )

            for child in composite.children:
                self.play(child.animation)

            try:
                self.play(
                    FadeOut(*self.mobjects),
                    run_time=composite.override_end_time,
                )
            except AttributeError:
                # FIXME: THIS IS A WORKAROUND!
                self.play(
                    FadeOut(*self.mobjects),
                    run_time=0.5,
                )

            try:
                self.play(
                    FadeIn(*mobjects_on_screen_before_animation),
                    run_time=composite.override_end_time,
                )
            except AttributeError:
                # FIXME: THIS IS A WORKAROUND!
                self.play(
                    FadeIn(*mobjects_on_screen_before_animation),
                    run_time=0.5,
                )

        return inner

    def add_base_animations(self) -> None:
        for section_name, func in self.animation_spec.items():
            if self.aligned_animation_scene.component_uses_code_timing(section_name):
                self.aligned_animation_scene.apply_code_timing(
                    section_name,
                    func,
                )
            else:
                if self._func_does_output_list_of_funcs(func):
                    list_of_funcs = func()
                    for i, anim_func in enumerate(list_of_funcs):
                        parent_of_animations = self.aligned_animation_scene.get_child(
                            section_name,
                        )
                        parent_of_animations.add_animation(
                            unique_id=i,
                            func=anim_func,
                            animation=anim_func(),
                            is_overriding_animation=False,
                        )
                else:
                    self.aligned_animation_scene.add_animation(
                        unique_id=section_name,
                        func=func,
                        animation=func(),
                        is_overriding_animation=False,
                    )

    def _func_does_output_list_of_funcs(self, func: Callable) -> bool:
        poorly_named_var = func()
        if isinstance(poorly_named_var, Iterable):
            for elem in poorly_named_var:
                if isinstance(elem, type(func)):
                    return True

        return False
