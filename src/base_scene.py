from manim import Scene, config, Animation, FadeOut, FadeIn, Succession, Wait
from script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript
from scene_scheduler import SceneScheduler

from abc import ABC, abstractmethod
import dill
import types

from typing import Iterable

class BaseScene(ABC, Scene):
    config.background_color = '#000E15'
    def __init__(self, problem_dir, aligned_animation_scene: CompositeAnimationScript):
        Scene.__init__(self)
        self.__aligned_animation_scene = aligned_animation_scene
        self.__problem_dir = problem_dir
        self._animation_spec = None
        self._scene_scheduler = SceneScheduler(self.__aligned_animation_scene)
        self._mobjects_pickle = 'mobjects_pickle.pkl'

    # NOTE: This may not work with multiple scenes!!!
    # NOTE: May have to name mangle self._animation_spec
    def setup(self):
        # Add animations from self._animation_spec to self.__aligned_animation_scene
        for section_name, animations in self._animation_spec.items():
            if self.__aligned_animation_scene.add_animations(unique_id=section_name, animations=animations, is_overriding_animation=False):
                raise RuntimeError(f'Unable to add animation for {section_name}')

        
        rolled_up_animations = self._scene_scheduler.schedule()

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
            if isinstance(obj, types.FunctionType):
                obj()
            else:
                self.play(obj.animation)

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