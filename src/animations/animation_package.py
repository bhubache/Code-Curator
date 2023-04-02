# '''
# In an attempt to make the animations of a data structure editable, we're going to modularize the animation
# into an AnimationPackage. It will be made of subpackages that will contain the animation in terms of alpha.
# ConcurrentPackage
# SuccessivePackage
# AlphaAnimator
# Ex:
#     Part way through the removal of a node in a linked list, we indicate the value
#     in the node to be removed.


# - run_time
# - num_animations
# '''

# # TODO: REALLY TRY TO KEEP THIS LINEAR!!!
# # NOTE: I don't know if that's best actually
# from __future__ import annotations

# import pandas as pd

# from .singly_linked_list.subanimations.base_subanimation import BaseSubanimation
# from .subanimation_group import SubanimationGroup
# from .singly_linked_list.subanimations.empty import Empty
# from manim import Mobject, Animation, Scene, VGroup, AnimationGroup

# from custom_logging.custom_logger import CustomLogger
# logger = CustomLogger.getLogger(__name__)

# class AnimationPackage:
#     def __init__(self, mobject: Mobject) -> None:
#         self._mobject: Mobject = mobject
#         self._subanimation_group: SubanimationGroup = SubanimationGroup(lag_ratio=1)
#         self._alpha_thresholds: dict = None
#         self._alpha_step_size: float = None
#         self._subanimation_group_started: list = []

#         self._mobject_copy_map = {}

#     def begin(self):
#         self._alpha_thresholds = {
#             index: (index + 1) / self.get_num_subanimations()
#             for index, _ in enumerate(self._subanimation_group)
#         }
#         self._alpha_step_size = 1 / self.get_num_subanimations()
#         self._subanimation_group_started = [False for _ in self._subanimation_group]

#         self._subanimation_group.init_run_time()

#     # TODO: Consider renaming the subanimation's begin method if it isn't going to be called in AnimationPackage.begin()
#     def interpolate_mobject(self, alpha: float):
#         self._subanimation_group.interpolate(alpha)


#         # animation_index = self._get_animation_index(alpha)
#         # normalized_alpha = self._get_normalized_alpha(alpha, animation_index)
#         # subanimation_list = self._subanimation_group[animation_index]

#         # if not self._animation_started(animation_index):
#         #     for subanimation in subanimation_list:
#         #         subanimation.begin()
#         #     self._mark_animation_started(animation_index)

#         # for subanimation in subanimation_list:
#         #     subanimation.interpolate(normalized_alpha)

#         #     if self._animation_is_over(normalized_alpha):
#         #         subanimation.clean_up_from_animation()

#     def clean_up_from_scene(self, scene: Scene):
#         self._subanimation_group.clean_up_from_scene(scene)
#         # for subanimation_list in self._subanimation_group:
#         #     for subanimation in subanimation_list:
#         #         subanimation.clean_up_from_scene(scene)

#     # def copy(self) -> AnimationPackage:
#     #     return copy.deepcopy(self)

#     def _get_normalized_alpha(self, alpha: float, animation_index: int) -> float:
#         end_alpha = self._alpha_thresholds[animation_index]
#         start_alpha = end_alpha - self._alpha_step_size

#         normalized_alpha = (alpha - start_alpha) / self._alpha_step_size
#         if normalized_alpha > 1:
#             return 1
#         return normalized_alpha

#     def _get_animation_index(self, alpha: float) -> int | None:
#         for index, upper_bound in self._alpha_thresholds.items():
#             if alpha <= upper_bound:
#                 return index
#         return None

#     def _animation_is_over(self, normalized_alpha: float) -> bool:
#         return round(normalized_alpha, 3) == 1

#     def _animation_started(self, index: int) -> bool:
#         return self._subanimation_group_started[index]

#     def _mark_animation_started(self, index: int) -> None:
#         self._subanimation_group_started[index] = True

#     def prepend_subanimation(self, subanimation: BaseSubanimation) -> None:
#         self._subanimation_group.insert(0, subanimation)
#         # subanimations_to_prepend.reverse()
#         # for subanimation in subanimations_to_prepend:
#         #     self._subanimation_group.insert(0, subanimation)

#     # FIXME: We want to make a new subanimation group that's concurrent and takes the last subanimation currently as well
#     def add_concurrent_subanimations(self, *subanimations_to_add: BaseSubanimation) -> None:
#         if self._last_subanimation_group_is_successive():
#             # self._subanimation_group.add(SubanimationGroup())
#             self._subanimation_group.get(-1)._lag_ratio = 0

#         for subanimation in subanimations_to_add:
#             self._subanimation_group.get(-1).add(subanimation)
#             # self.get_subanimation_group(index=-1).add(subanimation)

#     def _last_subanimation_group_is_successive(self) -> bool:
#         last_subanimation = self._subanimation_group.get(-1)
#         return last_subanimation._lag_ratio == 1


#     def add_successive_subanimations(self, *subanimations_to_add: BaseSubanimation) -> None:
#         # if not self._last_subanimation_group_is_successive():
#         #     self._subanimation_group.add(SubanimationGroup(lag_ratio=1))

#         # for subanimation in subanimations_to_add:
#         #     self._subanimation_group.get(-1).add(subanimation)

#         self._subanimation_group.add(
#             *[SubanimationGroup(subanimation, lag_ratio=1) for subanimation in subanimations_to_add]
#         )

#     ###################################################################################################################

#     # def create_ending_subanimation_slls(self, successive_package):
#     #     '''
#     #     When an animation group animates the same object multiple times at once, undesirable
#     #     behavior can occur. If we step through each subanimation successively and give each group
#     #     an sll that has all the qualities of the what their sll should like at the conclusion of
#     #     their subanimation group, they should be able to perform their animations correctly.
#     #     '''
#     #     # Iterate through self._subanimation_group, for all subanimations that are alone in their group
#     #     # or are orthogonal to all the subanimations in their group, use the successive subanimation. For
#     #     # subanimations that are not orthogonal in a group, they need to use the non-successive version
#     #     # and be given the target mobject at the conclusion of their group's subanimations.
#     #     interdependent_subanimations: list[BaseSubanimation] = self._get_interdependent_subanimations()

#     #     if self._no_interdependent_subanimations(interdependent_subanimations):
#     #         return

#     #     self._sub_in_successive_animations(interdependent_subanimations)

#     #     self._assign_forecasted_mobjects_for_subanimations(successive_package)

#     #     self._move_sll_subanimations_to_beginning_of_group()

#     # def _get_interdependent_subanimations(self) -> list[BaseSubanimation]:
#     #     interdepenent_subanimations = []

#     #     for group in self._subanimation_group:
#     #         if len(group) <= 1: continue

#     #         # Check every pair of subanimations for interdependency
#     #         for i, _ in enumerate(group):
#     #             for j, _ in enumerate(group):
#     #                 if i == j: continue

#     #                 if self._subanimation_pair_is_interdependent(group[i], group[j]):
#     #                     if group[i] not in interdepenent_subanimations:
#     #                         interdepenent_subanimations.append(group[i])
#     #                     if group[j] not in interdepenent_subanimations:
#     #                         interdepenent_subanimations.append(group[j])
#     #     return interdepenent_subanimations

#     # def _subanimation_pair_is_interdependent(self, first_sub: BaseSubanimation, second_sub: BaseSubanimation) -> bool:
#     #     subanimations_to_ignore = ['FadeInMobject', 'FadeOutMobject']
#     #     first_sub_name = first_sub.__class__.__name__
#     #     second_sub_name = second_sub.__class__.__name__
#     #     if first_sub_name in subanimations_to_ignore or second_sub_name in subanimations_to_ignore:
#     #         return False

#     #     df_subanimation_orth = pd.read_csv(
#     #         r'C:\Users\brand\Documents\ManimCS\src\animations\singly_linked_list\subanimations\subanimation_interdependency.csv',
#     #         index_col=0,
#     #     )

#     #     first_order_interdependency = df_subanimation_orth.at[first_sub_name, second_sub_name]
#     #     second_order_interdependency = df_subanimation_orth.at[second_sub_name, first_sub_name]

#     #     order_interdependencies_to_check = [first_order_interdependency, second_order_interdependency]

#     #     return 'yes' in order_interdependencies_to_check

#     # def _no_interdependent_subanimations(self, interdepenent_subanimations: list[BaseSubanimation]) -> bool:
#     #     return len(interdepenent_subanimations) == 0

#     # def _sub_in_successive_animations(self, interdependent_subanimations: list[BaseSubanimation]) -> None:
#     #     for subanimation_list in self._subanimation_group:
#     #         for i, subanimation in enumerate(subanimation_list):
#     #             if subanimation in interdependent_subanimations:
#     #                 continue

#     #             subanimation_list[i] = subanimation.create_successive_counterpart()

#     # def _assign_forecasted_mobjects_for_subanimations(self, successive_package: AnimationPackage) -> None:
#     #     successive_group_index = 0
#     #     for actual_group_index, actual_subanimation_group in enumerate(self._subanimation_group):
#     #         num_subanimations_in_actual_group = len(actual_subanimation_group)
#     #         last_successive_subanimation_of_group = None

#     #         completed_successive_subanimations = []

#     #         self._assign_forecasted_mobjects_for_group_at(actual_group_index, successive_package)

#     #         successive_group_index += num_subanimations_in_actual_group

#     # def _assign_forecasted_mobjects_for_group_at(self, actual_group_index: int, successive_package: AnimationPackage):
#     #     last_successive_subanimation_of_group: BaseSubanimation = None
#     #     completed_successive_subanimations: list[BaseSubanimation] = []
#     #     for successive_group_index in range(self._forecasted_get_start_index(actual_group_index), self._forecasted_get_end_index(actual_group_index)):
#     #         successive_subanimation = self._forecasted_get_subanimation_at(successive_group_index, successive_package)
#     #         last_successive_subanimation_of_group = self._mimic_animation_of_subanimation(successive_subanimation)
#     #         completed_successive_subanimations.append(last_successive_subanimation_of_group)

#     #     self._assign_forecasted_mobjects_for_group(
#     #         actual_subanimation_group=self._subanimation_group[actual_group_index],
#     #         last_successive_subanimation_of_group=last_successive_subanimation_of_group,
#     #         completed_successive_subanimations=completed_successive_subanimations
#     #     )

#     # def _forecasted_get_start_index(self, actual_group_index: int) -> int:
#     #     forecasted_index: int = 0
#     #     for group_index, group in enumerate(self._subanimation_group):
#     #         if group_index == actual_group_index:
#     #             break

#     #         for _ in group:
#     #             forecasted_index += 1
#     #     return forecasted_index

#     # def _forecasted_get_end_index(self, actual_group_index: int) -> int:
#     #     forecasted_index: int = 0
#     #     for group_index, group in enumerate(self._subanimation_group):
#     #         for _ in group:
#     #             forecasted_index += 1

#     #         if group_index == actual_group_index:
#     #             break
#     #     return forecasted_index

#     # def _forecasted_get_subanimation_at(self, group_index: int, successive_package: AnimationPackage) -> BaseSubanimation:
#     #     return successive_package._subanimation_lists[group_index][0]

#     # def _mimic_animation_of_subanimation(self, successive_subanimation: BaseSubanimation) -> BaseSubanimation:
#     #     successive_subanimation.begin()
#     #     successive_subanimation.interpolate(1)
#     #     successive_subanimation.clean_up_from_animation()
#     #     return successive_subanimation

#     # def _assign_forecasted_mobjects_for_group(
#     #     self,
#     #     actual_subanimation_group: list[BaseSubanimation],
#     #     last_successive_subanimation_of_group: BaseSubanimation,
#     #     completed_successive_subanimations: list[BaseSubanimation]
#     # ) -> None:
#     #     last_successive_subanimation_of_group_sll = last_successive_subanimation_of_group._sll
#     #     assert len(actual_subanimation_group) == len(completed_successive_subanimations)
#     #     for actual_subanimation, finished_subanimation in zip(actual_subanimation_group, completed_successive_subanimations):
#     #         # Copies necessary to save the state of the mobjects after each subanimation group
#     #         actual_subanimation.sll_post_subanimation_group = last_successive_subanimation_of_group_sll.copy()
#     #         actual_subanimation.finished_subanimation = finished_subanimation.copy()

#     # def _move_sll_subanimations_to_beginning_of_group(self):
#     #     for list_index, subanimation_list in enumerate(self._subanimation_group):
#     #         sll_subanimations = []
#     #         for i, subanimation in enumerate(subanimation_list):
#     #             if subanimation._animates_sll:
#     #                 sll_subanimations.append(subanimation)

#     #         for subanimation in sll_subanimations:
#     #             self._subanimation_group[list_index].remove(subanimation)

#     #         for subanimation in sll_subanimations:
#     #             self._subanimation_group[list_index].insert(0, subanimation)

#     def get_run_time(self) -> float:
#         return self._subanimation_group.get_run_time()

#     # NOTE: Keep a watchful eye, removing the empty animations may need to be moved somewhere else, like earlier in the call chain
#     def get_num_subanimations(self) -> int:
#         return self._subanimation_group.get_num_subanimations()

#         # Remove all Empty subanimations
#         # subanimation_lists_without_empty = []
#         # for group_index, subanimation_group in enumerate(self._subanimation_group):
#         #     new_subanimation_group = []
#         #     for subanimation_index, subanimation in enumerate(subanimation_group):
#         #         if isinstance(subanimation, Empty):
#         #             continue

#         #         new_subanimation_group.append(subanimation)

#         #     if len(new_subanimation_group) != 0:
#         #         subanimation_lists_without_empty.append(new_subanimation_group)

#         # self._subanimation_group = subanimation_lists_without_empty

#         # return len(self._subanimation_group)

#     def create_subanimation_group_successive_counterpart(self) -> SubanimationGroup:
#         return self._subanimation_group.sub_in_successive_counterparts()

#     def create_successive_subanimation_group(self) -> SubanimationGroup:
#         return self._subanimation_group.create_successive_counterpart()

#     def get_subanimation_group(self) -> list[SubanimationGroup]:
#         return self._subanimation_group

#     def set_all_subanimation_groups(self, new_subanimation_groups: list[SubanimationGroup]) -> None:
#         self._subanimation_group = new_subanimation_groups

#     def get_subanimation_group(self) -> SubanimationGroup:
#         return self._subanimation_group

#     def get_subanimation(self, group_index: int, subanimation_index: int) -> BaseSubanimation:
#         return self._subanimation_group[group_index].get(index=subanimation_index)

#     def set_subanimation(self, index: int, subanimation: BaseSubanimation) -> None:
#         self._subanimation_group.set(index=index, subanimation=subanimation)
#         # self._subanimation_group[group_index].set(index=subanimation_index, subanimation=subanimation)

#     def remove_subanimation(self, group_index: int, subanimation: BaseSubanimation) -> None:
#         self._subanimation_group[group_index].remove(subanimation=subanimation)

#     def set_subanimation_group(self, new_subanimation_group: SubanimationGroup) -> None:
#         self._subanimation_group = new_subanimation_group

#     # def prepend_subanimation(self, group_index: int, subanimation: BaseSubanimation) -> None:
#     #     self._subanimation_group[group_index].insert(0, subanimation)
#         # self._subanimation_group[group_index][subanimation_index] = subanimation

#     # @property
#     # def subanimation_groups(self) -> list[list[BaseSubanimation]]:
#     #     return self._subanimation_group

#     # @subanimation_groups.setter
#     # def subanimation_groups(self, new_subanimation_groups: list[list[BaseSubanimation]]) -> None:
#     #     self._subanimation_group = new_subanimation_groups
