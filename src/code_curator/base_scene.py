from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Callable

from code_curator.custom_logging.custom_logger import CustomLogger
from manim import config
from manim import FadeIn
from manim import FadeOut
from manim import Scene
from code_curator.scene_scheduler import SceneScheduler
from code_curator.script_handling.components.animation_script.animation_leaf import AnimationLeaf
from code_curator.script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript
logger = CustomLogger.getLogger(__name__)


class BaseScene(ABC, Scene):
    """Test docstring

    :param ABC: _description_
    :type ABC: _type_
    :param Scene: _description_
    :type Scene: _type_
    :raises RuntimeError: _description_
    :return: _description_
    :rtype: _type_
    """
    config.background_color = '#000E15'

    def __init__(self, problem_dir: str, aligned_animation_scene: CompositeAnimationScript) -> None:
        Scene.__init__(self)
        self._aligned_animation_scene: CompositeAnimationScript = aligned_animation_scene
        self._problem_dir: str = problem_dir
        self._animation_spec: dict = {}
        self._scene_scheduler: SceneScheduler = SceneScheduler()
        self._mobjects_pickle: str = 'mobjects_pickle.pkl'

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

    # NOTE: This may not work with multiple scenes!!!
    def setup(self) -> None:
        rolled_up_animations = self.scene_scheduler.schedule(
            self.aligned_animation_scene,
        )

        for i, composite in enumerate(rolled_up_animations):
            if composite.is_overriding_animation:
                rolled_up_animations[i] = self.super_add_overriding_animation(
                    composite,
                )

        self._animations = rolled_up_animations

    def construct(self) -> None:
        for obj in self._animations:
            if isinstance(obj, AnimationLeaf):
                obj.func()
                print(obj.animation)
                print(obj.animation.run_time)
                self.play(obj.animation)
            elif callable(obj):
                print(obj)
                obj()
            else:
                raise RuntimeError(
                    f'Unexpected type {type(obj)} when running animations: {obj}',
                )

    def tear_down(self) -> None:
        self.play(FadeOut(*self.mobjects))

    @abstractmethod
    def create_animation_spec(self) -> dict:
        pass

    def super_add_overriding_animation(self, composite: CompositeAnimationScript) -> Callable:
        def inner() -> None:
            mobjects_on_screen_before_animation = self.mobjects.copy()

            self.play(
                FadeOut(*self.mobjects),
                run_time=composite.override_start_time,
            )

            for child in composite.children:
                self.play(child.animation)

            self.play(
                FadeOut(*self.mobjects),
                run_time=composite.override_end_time,
            )

            self.play(
                FadeIn(*mobjects_on_screen_before_animation),
                run_time=composite.override_end_time,
            )
        return inner

    def add_base_animations(self) -> None:
        for section_name, func in self.animation_spec.items():
            if self.aligned_animation_scene.component_uses_code_timing(section_name):
                self.aligned_animation_scene.apply_code_timing(
                    section_name, func,
                )
            else:
                if self._func_outputs_list_of_funcs(func):
                    list_of_funcs = func()
                    for i, anim_func in enumerate(list_of_funcs):
                        self.aligned_animation_scene.add_animation(
                            unique_id=f'{section_name}_{i}',
                            func=anim_func, animation=anim_func(),
                            is_overriding_animation=False,
                        )
                else:
                    self.aligned_animation_scene.add_animation(
                        unique_id=section_name,
                        func=func, animation=func(),
                        is_overriding_animation=False,
                    )

    def _func_outputs_list_of_funcs(self, func: Callable) -> bool:
        poorly_named_var = func()
        for elem in poorly_named_var:
            if isinstance(elem, type(func)):
                return True
        return False
