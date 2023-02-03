from manim import Wait, AnimationGroup, Animation

from typing import Iterable

from ..base_scene import BaseScene

class SceneScheduler:
    def __init__(self, animation_spec, aligned_animation_script):
        self._animation_spec = animation_spec
        self._aligned_animation_script = aligned_animation_script
        self._fade_time = 1

    def schedule(self):
        scheduled_animations = []

        methods_and_timing_info = self.zip_spec_and_script()

        for i, (curr_method, timing_info) in enumerate(methods_and_timing_info):
            next_method = None if i + 1 == len(methods_and_timing_info) else methods_and_timing_info[i + 1][0]

            curr_is_overriding_animation = hasattr(curr_method, 'is_overriding_animation')
            next_is_overriding_animation = hasattr(next_method, 'is_overriding_animation')
                
            if curr_method is None:
                curr_allotted_run_time = None
                if isinstance(timing_info, list):
                    curr_allotted_run_time = timing_info[0].get('duration')
                else:
                    curr_allotted_run_time = timing_info.get('duration')
                if hasattr(next_method, 'is_overriding_animation'):
                    # If next animation is an overriding animation, we need to FadeOut at the end of this animation for self._fade_time
                    if curr_allotted_run_time - self._fade_time < 0:
                        raise RuntimeError('Curr RUN TIME DOES NOT HAVE ENOUGH TIME TO ALLOCATE 1 SECOND OF FADING OUT')
                    
                    curr_allotted_run_time -= self._fade_time

                    group_of_animations = []
                    group_of_animations.append(Wait(curr_allotted_run_time))
                    scheduled_animations.append(OverridingAnimationInfo(
                        animations=group_of_animations,
                        is_overriding_animation=False,
                        next_is_overriding_animation=True,
                        is_overriding_fade_out_time=0,
                        next_is_overriding_fade_time=self._fade_time)
                    )
                else:
                    scheduled_animations.append(Wait(curr_allotted_run_time))
                continue

            animations = curr_method()
                

            group_of_animations = []
            for sub_anim_index, (anim, timing) in enumerate(zip(animations, timing_info)):
                # Handle AnimationBuilder
                if not isinstance(anim, Animation):
                    anim = anim.build()

                allotted_run_time = timing.get('duration')
                anim_run_time = anim.run_time

                if allotted_run_time - anim_run_time < 0:
                    # raise RuntimeError('Animation doesn\'t fit within allotted time')

                    # NOTE: The logic might not be correct here
                    if not next_is_overriding_animation and next_method is not None:
                        methods_and_timing_info[i + 1][1]['duration'] -= anim_run_time
                        allotted_run_time += anim_run_time
                    else:
                        print('Animation doesn\'t fit within allotted time')
                else:
                    allotted_run_time -= anim_run_time
                

                if sub_anim_index == len(animations) - 1:
                    if curr_is_overriding_animation:
                        if allotted_run_time - self._fade_time < 0:
                            raise RuntimeError('Current overriding animation no fit')

                        allotted_run_time -= self._fade_time

                    if next_is_overriding_animation:
                        if allotted_run_time - self._fade_time < 0:
                            raise RuntimeError('Next overriding animation no fit')

                        allotted_run_time -= self._fade_time

                group_of_animations = []

                group_of_animations.append(anim) 
                group_of_animations.append(Wait(allotted_run_time))

            if curr_is_overriding_animation or next_is_overriding_animation:
                scheduled_animations.append(
                        OverridingAnimationInfo(
                            animations=group_of_animations,
                            is_overriding_animation=curr_is_overriding_animation,
                            next_is_overriding_animation=next_is_overriding_animation,
                            is_overriding_fade_out_time=self._fade_time if curr_is_overriding_animation else 0,
                            next_is_overriding_fade_time=self._fade_time if next_is_overriding_animation else 0
                        )
                    )
            else:
                scheduled_animations.append(group_of_animations)
                
        return scheduled_animations

    def _add_animation(self, *values, my_list):
        for val in values:
            my_list.append(lambda : val)

    def zip_spec_and_script(self) -> Iterable[tuple]:
        zipped = []
        spec_intro_info = self._animation_spec['intro']
        script_intro_values = self._get_script_timing_iterable('<intro>')
        for order_method in spec_intro_info.values():
            if order_method is None: continue

            zipped.append((order_method, [next(script_intro_values)]))

        spec_explanation_info = self._animation_spec['explanation']
        
        # TODO: Account for pre explanation
        # TODO: Account for post explanation

        explanation_spec_info = spec_explanation_info['during']
        script_explanation_values = self._get_explanation_timing_iterable()

        for explanation_spec, script_explanation in zip(explanation_spec_info.values(), script_explanation_values):
            spec_order_keys = explanation_spec.keys().__iter__()
            spec_order = next(spec_order_keys)
            for script_order in script_explanation:
                if script_order != spec_order:
                    zipped.append((None, script_explanation[script_order]))
                else:
                    # If there's only one timing info for this order
                    if script_explanation[script_order].get('text') is not None:
                        zipped.append((explanation_spec[spec_order], [script_explanation[script_order]]))
                    else:
                        zipped.append((explanation_spec[spec_order], list(script_explanation[script_order].values())))
                    spec_order = next(spec_order_keys)
        return zipped

    def _get_script_timing_iterable(self, key):
        # If the value is a dict, then there is only one curr_method in that order mapping to <during> (probably)
        if isinstance(self._aligned_animation_script[key], dict):
            return [self._aligned_animation_script[key]].__iter__()
        return self._aligned_animation_script[key].values().__iter__()

    def _get_explanation_timing_iterable(self):
        explanations = []
        explanation_key = '<explanation_{}>'
        for i, key in enumerate(self._aligned_animation_script):
            explanation_dict = self._aligned_animation_script.get(explanation_key.format(i))
            if explanation_dict is not None:
                explanations.append(explanation_dict)
        return explanations


class OverridingAnimationInfo:
    def __init__(self, animations: Iterable, is_overriding_animation, next_is_overriding_animation, is_overriding_fade_out_time, next_is_overriding_fade_time):
        self._animations = animations
        self._is_overriding_animation = is_overriding_animation
        self._next_is_overriding_animation = next_is_overriding_animation
        self._is_overriding_fade_out_time = is_overriding_fade_out_time
        self._next_is_overriding_fade_time = next_is_overriding_fade_time

    @property
    def animations(self):
        return self._animations

    @property
    def is_overriding_animation(self):
        return self._is_overriding_animation

    @property
    def next_is_overriding_animation(self):
        return self._next_is_overriding_animation

    @property
    def is_overriding_fade_out_time(self):
        return self._is_overriding_fade_out_time

    @property
    def next_is_overriding_fade_time(self):
        return self._next_is_overriding_fade_time

