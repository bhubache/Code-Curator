'''
In an attempt to make the animations of a data structure editable, we're going to modularize the animation
into an AnimationPackage. It will be made of subpackages that will contain the animation in terms of alpha.
ConcurrentPackage
SuccessivePackage
AlphaAnimator
Ex:
    Part way through the removal of a node in a linked list, we indicate the value
    in the node to be removed.


- run_time
- num_animations
'''

# TODO: REALLY TRY TO KEEP THIS LINEAR!!!
from __future__ import annotations
import copy

import pandas as pd
from manim import Mobject, Animation, Scene

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class AnimationPackage:
    def __init__(self, mobject: Mobject) -> None:
        self._mobject: Mobject = mobject
        self._subanimation_lists: list[list[Animation]] = []
        self._alpha_thresholds: dict = None
        self._alpha_step_size: float = None
        self._subanimation_groups_started: list = []

    def begin(self):
        self._alpha_thresholds = {
            index: (index + 1) / self.get_num_animations()
            for index, _ in enumerate(self._subanimation_lists)
        }
        self._alpha_step_size = 1 / self.get_num_animations()
        self._subanimation_groups_started = [False for _ in self._subanimation_lists]

    def interpolate_mobject(self, alpha: float):
        animation_index = self._get_animation_index(alpha)
        normalized_alpha = self._get_normalized_alpha(alpha, animation_index)
        subanimation_list = self._subanimation_lists[animation_index]

        logger.info(id(self._mobject))

        if not self._animation_started(animation_index):
            for subanimation in subanimation_list:
                logger.info(id(subanimation._sll))
                subanimation.begin()
            self._mark_animation_started(animation_index)

        for subanimation in subanimation_list:
            subanimation.interpolate(normalized_alpha)

            if self._animation_is_over(normalized_alpha):
                subanimation.clean_up_from_animation()

    def clean_up_from_scene(self, scene: Scene):
        for subanimation_list in self._subanimation_lists:
            for subanimation in subanimation_list:
                subanimation.clean_up_from_scene(scene)

    def copy(self) -> AnimationPackage:
        return copy.deepcopy(self)

    def _get_normalized_alpha(self, alpha: float, animation_index: int) -> float:
        end_alpha = self._alpha_thresholds[animation_index]
        start_alpha = end_alpha - self._alpha_step_size

        normalized_alpha = (alpha - start_alpha) / self._alpha_step_size
        if normalized_alpha > 1:
            return 1
        return normalized_alpha
        
    def _get_animation_index(self, alpha: float) -> int | None:
        for index, upper_bound in self._alpha_thresholds.items():
            if alpha <= upper_bound:
                return index
        return None
    
    def _animation_is_over(self, normalized_alpha: float) -> bool:
        return round(normalized_alpha, 3) == 1

    def _animation_started(self, index: int) -> bool:
        return self._subanimation_groups_started[index]
    
    def _mark_animation_started(self, index: int) -> None:
        self._subanimation_groups_started[index] = True
    
    def prepend_concurrent_animations(self, *animations: Animation) -> None:
        subanimations_list = [subanimation for subanimation in animations]
        self._subanimation_lists.insert(0, subanimations_list)
        
    def prepend_successive_animations(self, *animations: Animation) -> None:
        subanimations_list = [subanimation for subanimation in animations]
        subanimations_list.reverse()
        for subanimation in subanimations_list:
            self._subanimation_lists.insert(0, [subanimation])
    
    def append_concurrent_animations(self, *animations: Animation) -> None:
        subanimations_list = []
        for subanimation in animations:
            subanimations_list.append(subanimation)
        self._subanimation_lists.append(subanimations_list)

    def append_successive_animations(self, *animations: Animation) -> None:
        for subanimation in animations:
            self._subanimation_lists.append([subanimation])

    def _convert_to_successive_subanimations(self) -> AnimationPackage:
        # TODO: Check to make sure that self_copy was recursively copied
        successive_animation_package = AnimationPackage(self._mobject)
        for subanimation_list in self._subanimation_lists:
            for subanimation in subanimation_list:
                successive_animation_package.append_successive_animations(subanimation.create_successive_counterpart())
        return successive_animation_package

    def create_ending_subanimation_slls(self):
        '''
        When an animation group animates the same object multiple times at once, undesirable
        behavior can occur. If we step through each subanimation successively and give each group
        an sll that has all the qualities of the what their sll should like at the conclusion of 
        their subanimation group, they should be able to perform their animations correctly.
        '''
        # Iterate through self._subanimation_lists, for all subanimations that are alone in their group
        # or are orthogonal to all the subanimations in their group, use the successive subanimation. For
        # subanimations that are not orthogonal in a group, they need to use the non-successive version
        # and be given the target mobject at the conclusion of their group's subanimations.
        from pprint import pprint
        pprint(self._subanimation_lists)
        df_subanimation_orth = pd.read_csv(r'C:\Users\brand\Documents\ManimCS\src\animations\singly_linked_list\subanimations\subanimation_orthogonality.csv')
        print(df_subanimation_orth)
        # Same subanimations as self but every subanimation is successive
        successive_package = self._convert_to_successive_subanimations()
        successive_group_index = 0
        for _, actual_subanimation_group in enumerate(self._subanimation_lists):
            num_subanimations_in_actual_group = len(actual_subanimation_group)
            last_successive_subanimation_of_group = None

            for i in range(successive_group_index, successive_group_index + num_subanimations_in_actual_group):
                successive_subanimation = successive_package._subanimation_lists[i][0]
                successive_subanimation.begin()
                successive_subanimation.interpolate(1)
                successive_subanimation.clean_up_from_animation()
                successive_subanimation._sll.save_state()
                last_successive_subanimation_of_group = successive_subanimation

            successive_group_index += num_subanimations_in_actual_group

            sll_at_conclusion_of_subanimation_group = last_successive_subanimation_of_group._sll.copy()
            for actual_subanimation in actual_subanimation_group:
                actual_subanimation.sll_post_subanimation_group = sll_at_conclusion_of_subanimation_group

    def get_num_animations(self) -> int:
        return len(self._subanimation_lists)