from manim import *

from abc import ABC, abstractmethod
import dill

from typing import Iterable

class BaseScene(ABC, Scene):
    config.background_color = '#000E15'
    def __init__(self, problem_dir):
        Scene.__init__(self)
        self.__problem_dir = problem_dir
        self._animation_spec = None
        self._mobjects_pickle = 'mobjects_pickle'

    def setup(self):
        pass

    def construct(self):
        pass

    def tear_down(self):
        self.play(FadeOut(*self.mobjects))

    @abstractmethod
    def _schedule_scene(self):
        pass

    def run_animations(self, animation_spec = None):
        if animation_spec is None:
            animation_spec = self._animation_spec
        for section, animation_chunk in animation_spec.items():
            for order, animation in animation_chunk.items():
                if animation is None: continue

                if isinstance(animation, dict):
                    self.run_animations(animation)
                    continue

                anim_obj = animation()
                if anim_obj is not None:
                    self.play(anim_obj)

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

    def add_animation(self, section, order, animation, constraint_num = None, constraint_order = None):
        callable_animation = animation
        if not callable(animation):
            callable_animation = lambda : animation
        if section not in self._animation_spec:
            raise KeyError(f'{section} is not a valid key for animation_spec')
        
        if order not in self._animation_spec[section]:
            raise KeyError(f'{order} is not a valid key for the section')

        if section == 'constraints' and order == 'during':
            if constraint_num not in self._animation_spec[section][order]:
                raise KeyError(f'{constraint_num} is not a valid constraint number')

            if constraint_order not in self._animation_spec[section][order][constraint_num]:
                raise KeyError(f'{constraint_order} is not a valid constraint order')

            self._animation_spec[section][order][constraint_num][constraint_order] = callable_animation
        else:
            self._animation_spec[section][order] = callable_animation

    def add_overriding_animation(self, animation_info):
        def inner():
            # Save mobjects currently on screen so we can fade them back in after the animation
            if animation_info.next_is_overriding_animation:
                # pickle data
                mobjects_on_screen_before_animation = self.mobjects.copy()
                with open(self._mobjects_pickle, 'wb') as write_file:
                    print(mobjects_on_screen_before_animation)
                    dill.dump(mobjects_on_screen_before_animation, write_file)

            for animation in animation_info.animations:
                self.play(animation)

            if animation_info.next_is_overriding_animation:
                self.play(FadeOut(*self.mobjects), run_time=animation_info.next_is_overriding_fade_time)

            # FIXME: Fading time
            if animation_info.is_overriding_animation:
                with open(self._mobjects_pickle, 'rb') as read_file:
                    mobjects_on_screen_before_animation = dill.load(read_file)

                    # Fade out all mobjects involved with animation
                    self.play(FadeOut(*self.mobjects, run_time=animation_info.is_overriding_fade_out_time / 2))
                    self.play(FadeIn(*mobjects_on_screen_before_animation, run_time=animation_info.is_overriding_fade_out_time / 2))
        return inner

    def add_constraint_animation(self, animation, constraint_num, constraint_order = 'post'):
        return self.add_overriding_animation(section='constraints', order='during', animation=animation, constraint_num=constraint_num, constraint_order=constraint_order)

    def _add_animation(self, *keys, animation):
        self.dynamically_set_nested_dict(*keys, d=self._animation_spec, value=animation)

    def dynamically_set_nested_dict(self, *keys, d, value):
        last_key = keys[-1]
        for key in keys[:-1]:
            d = d[key]
        d[last_key] = value