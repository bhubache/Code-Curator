from abc import ABC, abstractmethod
import dill
import types
from typing import Iterable

from manim import Scene, config, Animation, FadeOut, FadeIn
from script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript
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

    def add_base_animations(self):
        for section_name, func in self._animation_spec.items():
            # If section uses code timing
            if self.aligned_animation_scene.component_uses_code_timing(section_name):
                self.aligned_animation_scene.convert_leaf_to_composite(section_name, func)
            else:
                self.aligned_animation_scene.add_animation(unique_id=section_name, func=func, animation=func(), is_overriding_animation=False)
            # Add animation(s)

    @property
    def aligned_animation_scene(self) -> CompositeAnimationScript:
        return self._aligned_animation_scene

    # NOTE: This may not work with multiple scenes!!!
    # NOTE: May have to name mangle self._animation_spec
    def setup(self):
        # Add animations from self._animation_spec to self._aligned_animation_scene
        # for section_name, func in self._animation_spec.items():
        #     if self._aligned_animation_scene.add_animation(unique_id=section_name, func=func, is_overriding_animation=False):
        #         raise RuntimeError(f'Unable to add animation for {section_name}')

        
        rolled_up_animations = self._scene_scheduler.schedule(self.aligned_animation_scene)

        for i, composite in enumerate(rolled_up_animations):
            if composite.is_overriding_animation:
                rolled_up_animations[i] = self.super_add_overriding_animation(composite)

        self._animations = rolled_up_animations

    def construct(self):
        self.run_animations()

    def tear_down(self):
        self.play(FadeOut(*self.mobjects))

    @abstractmethod
    def create_animation_spec(self):
        pass

    def run_animations(self):
        for obj in self._animations:
            logger.info(obj.unique_id)
            obj.func()
            self.play(obj.animation)
            # if isinstance(obj, types.FunctionType):
            #     obj()
            # else:
            #     self.play(obj.animation)

    # TODO: Timing aligned with script audio
    def _make_successive_animations(self, *animations) -> Animation:
        '''
        Takes in 
        '''
        return Succession(
                *[Succession(
                    anim if not isinstance(anim, Iterable) else AnimationGroup(*anim),
                    Wait(0)
                ) for anim in animations]
            )

    def super_add_overriding_animation(self, composite: CompositeAnimationScript):
        def inner():
            mobjects_on_screen_before_animation = self.mobjects.copy()

            self.play(FadeOut(*self.mobjects), run_time=composite.override_start_time)

            for child in composite.children:
                self.play(child.animation)

            self.play(FadeOut(*self.mobjects), run_time=composite.override_end_time)

            self.play(FadeIn(*mobjects_on_screen_before_animation), run_time=composite.override_end_time)
        return inner