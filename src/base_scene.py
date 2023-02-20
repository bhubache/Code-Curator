from abc import ABC, abstractmethod
import dill
import types
from typing import Iterable, Callable

from manim import Scene, config, Animation, FadeOut, FadeIn
from script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript
from script_handling.components.animation_script.animation_leaf import AnimationLeaf
from scene_scheduler import SceneScheduler

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class BaseScene(ABC, Scene):
    config.background_color = '#000E15'
    def __init__(self, problem_dir, aligned_animation_scene: CompositeAnimationScript):
        Scene.__init__(self)
        self._aligned_animation_scene = aligned_animation_scene
        self._problem_dir = problem_dir
        self._animation_spec = None
        self._scene_scheduler = SceneScheduler()
        self._mobjects_pickle = 'mobjects_pickle.pkl'

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
    def setup(self):
        rolled_up_animations = self.scene_scheduler.schedule(self.aligned_animation_scene)

        for i, composite in enumerate(rolled_up_animations):
            if composite.is_overriding_animation:
                rolled_up_animations[i] = self.super_add_overriding_animation(composite)

        self._animations = rolled_up_animations

    def construct(self):
        for obj in self._animations:
            if isinstance(obj, AnimationLeaf):
                obj.func()
                self.play(obj.animation)
            elif isinstance(obj, Callable):
                obj()
            else:
                raise RuntimeError(f'Unexpected type {type(obj)} when running animations')

    def tear_down(self):
        self.play(FadeOut(*self.mobjects))

    @abstractmethod
    def create_animation_spec(self):
        pass

    def super_add_overriding_animation(self, composite: CompositeAnimationScript):
        def inner():
            mobjects_on_screen_before_animation = self.mobjects.copy()

            self.play(FadeOut(*self.mobjects), run_time=composite.override_start_time)

            for child in composite.children:
                self.play(child.animation)

            self.play(FadeOut(*self.mobjects), run_time=composite.override_end_time)

            self.play(FadeIn(*mobjects_on_screen_before_animation), run_time=composite.override_end_time)
        return inner

    def add_base_animations(self):
        for section_name, func in self.animation_spec.items():
            if self.aligned_animation_scene.component_uses_code_timing(section_name):
                self.aligned_animation_scene.apply_code_timing(section_name, func)
            else:
                if self._func_outputs_list_of_funcs(func):
                    list_of_funcs = func()
                    for i, anim_func in enumerate(list_of_funcs):
                        self.aligned_animation_scene.add_animation(unique_id=f'{section_name}_{i}', func=anim_func, animation=anim_func(), is_overriding_animation=False)
                else:
                    self.aligned_animation_scene.add_animation(unique_id=section_name, func=func, animation=func(), is_overriding_animation=False)

    def _func_outputs_list_of_funcs(self, func: Callable) -> bool:
        l = func()
        for elem in l:
            if isinstance(elem, type(func)):
                return True
        return False