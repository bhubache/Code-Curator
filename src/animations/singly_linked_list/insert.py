from typing import Any
import math

from .base_sll_packager import BaseSLLPackager
from data_structures.singly_linked_list import singly_linked_list
from animations.singly_linked_list.add_first import AddFirst
from data_structures.nodes.singly_linked_list_node import SLLNode
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from data_structures.pointers.pointer import Pointer
from .subanimations.base_subanimation import BaseSubanimation
from ..animation_package import AnimationPackage
from ..package_animation import PackageAnimation
from .subanimations.fade_in_container import FadeInContainer
from .subanimations.fade_in_pointer import FadeInPointer
from .subanimations.grow_pointer import GrowPointer
from .subanimations.move_trav import MoveTrav
from .subanimations.center_sll import CenterSLL
from .subanimations.change_next_pointer import ChangeNextPointer
from .subanimations.flatten_list import FlattenList
from .subanimations.fade_in_trav import FadeInTrav
from .subanimations.fade_out_trav import FadeOutTrav
from .subanimations.shift_sub_list import ShiftSubList
from .subanimations.strictly_successive.shift_sub_list import SuccessiveShiftSubList
from .subanimations.strictly_successive.center_sll import SuccessiveCenterSLL
from manim import Animation, linear, smooth, Scene, LEFT, UP, DOWN, RIGHT, VGroup, Circle

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

# class _Insert:
#     def __init__(
#         self,
#         sll,
#         index:     int,
#         node:      SLLNode,
#         prev_node_pointer_to_next = None,
#         trav = None,
#         sll_group_to_shift = None,
#         mob_anims: dict = None,
#         run_time:  int = 1,
#         rate_func = linear,
#         **kwargs
#     ):
#         # import json
#         # print(json.dumps(mob_anims, indent=4, default=str))
#         run_time = len(mob_anims)
#         super().__init__(
#             sll,
#             index=index,
#             node=node,
#             run_time=run_time,
#             mob_groups=mob_anims,
#             rate_func=rate_func,
#             **kwargs
#         )
#         self.prev_node_pointer_to_next = prev_node_pointer_to_next
#         self.trav = trav
#         self.sll_group_to_shift = sll_group_to_shift
#         self.container = self.node.container
#         self.pointer_to_next = self.node.pointer_to_next

#     def begin(self):
#         self.sll.save_state()
#         self.node.save_state()
#         self.node.pointer_to_next.save_state()
#         self.sll.head_pointer.save_state()
#         self._save_state_prev_node_pointer_to_next()
#         self.sll_group_to_shift.save_state()
#         self.trav.save_state()

#         self.final_list_copy = singly_linked_list.SinglyLinkedList(*[node.data._value for node in self.sll])
#         self.shift_left_value = self.sll.get_left()[0] - self.final_list_copy.get_left()[0]

#         self.distance_to_shift = abs(self.sll[0].get_left() - self.sll[1].get_left())
#         self.distance_up = None
#         if self.index == 0:
#             self.distance_up = abs(self.node.get_container_top() - self.sll[1].get_container_top())
#         else:
#             self.distance_up = abs(self.node.get_container_top() - self.sll[0].get_container_top())

#         self.original_sll_location = self.sll.get_center()

#         self.node.container.set_opacity(0)
#         self.node.pointer_to_next.set_opacity(0)
#         super().begin()

#     def interpolate_mobject(self, alpha: float):
#         for animation_num, mob_group in self.mob_groups.items():
#             for animation_str, mob_info in mob_group.items():
#                 normalized_alpha = self._get_normalized_alpha(alpha, animation_num)

#                 if normalized_alpha <= 0 or normalized_alpha > 1:
#                     continue

#                 mobject = mob_info['mobject']

#                 if animation_str == 'trav_fade_in':
#                     self.trav.set_opacity(normalized_alpha)
#                     if round(normalized_alpha, 3) == 1:
#                         self.trav.save_state()
#                     # self.trav.save_state()
#                 elif animation_str == 'trave_fade_out':
#                     self.trav.set_opacity(1 - normalized_alpha)
#                 elif animation_str == 'trav_move':
#                     self.trav.restore()
#                     next_node = mob_info['next_node']
#                     self.trav.move_immediately_alpha(next_node, next_node, smooth(normalized_alpha))
#                     if round(normalized_alpha, 3) == 1:
#                         self.trav.save_state()
#                 elif animation_str == 'container_fade_in':
#                     self.container.set_stroke(opacity=normalized_alpha)
#                     for container_sub in self.container.submobjects:
#                         container_sub.set_opacity(normalized_alpha)
#                 elif animation_str == 'pointer_to_next_fade_in':
#                     self.pointer_to_next.set_opacity(normalized_alpha)
#                 elif animation_str == 'prev_node_pointer_to_next_move':
#                     self.prev_node_pointer_to_next.restore()
#                     original_start, original_end = self.prev_node_pointer_to_next.get_start_and_end()
#                     final_end = original_end + ((self.node.get_container_left() - original_end) * smooth(normalized_alpha))
#                     self.prev_node_pointer_to_next.become(
#                         SinglyDirectedEdge(
#                             start=original_start,
#                             end=final_end
#                         )
#                     )
#                 elif animation_str == 'shift_sub_list':
#                     self.sll.restore()
#                     self.node.restore()
#                     self.sll_group_to_shift.restore()
#                     self.sll.shift(LEFT * self.shift_left_value * smooth(alpha))
#                     self.sll_group_to_shift.shift(RIGHT * self.distance_to_shift * smooth(alpha))
#                 elif animation_str == 'flatten':
#                     self.sll.restore()
#                     self.node.restore()
#                     self.sll_group_to_shift.restore()
#                     self.trav.restore()
                    
#                     def flatten_list(self, alpha):
#                         # self.sll.restore()
#                         if self.index == 0:
#                             self.sll.shift(RIGHT * self.shift_left_value * smooth(alpha))
#                         else:
#                             self.sll.shift(LEFT * self.shift_left_value * smooth(alpha))

#                         # self.node.restore()
#                         if self.index == 0:
#                             self.node.shift(LEFT * self.shift_left_value * smooth(alpha) * 2)
#                         self.node.shift(UP * self.distance_up * smooth(alpha))

#                         # self.sll_group_to_shift.restore()
#                         # self.sll_group_to_shift.shift(LEFT * self.shift_left_value * smooth(alpha))
#                         self.sll_group_to_shift.shift(RIGHT * self.distance_to_shift * smooth(alpha))

#                         if self.prev_node_pointer_to_next is not None:
#                             self.prev_node_pointer_to_next.become(SinglyDirectedEdge(start=self.sll[self.index - 1].get_container_right(), end=self.sll[self.index].get_container_left()))

#                         self.trav.set_opacity(1 - alpha)

#                         def rotate_start():
#                             start, _ = self.node.pointer_to_next.get_start_and_end()
#                             curr_x = start[0]
#                             curr_y = start[1]

#                             origin_x, origin_y, _ = self.node.get_container_center()
#                             angle = -(math.pi / 2 * smooth(alpha))
#                             sine = math.sin(angle)
#                             cosine = math.cos(angle)

#                             new_x = origin_x + cosine * (curr_x - origin_x) - sine * (curr_y - origin_y)
#                             new_y = origin_y - sine * (curr_x - origin_x) + cosine * (curr_y - origin_y)
#                             return [new_x, new_y, 0]

#                         def rotate_end():
#                             # FIXME: Hardcoded bottom of container
#                             curr_x, curr_y, _ = self.sll[self.index + 1].get_container_bottom()

#                             angle = -(math.pi / 2 * smooth(alpha))
#                             sine = math.sin(angle)
#                             cosine = math.cos(angle)

#                             origin_x, origin_y, _ = self.sll[self.index + 1].get_container_center()
#                             curr_x = curr_x - origin_x
#                             curr_y = curr_y - origin_y

#                             new_x = curr_x * cosine - curr_y * sine
#                             new_y = curr_x * sine + curr_y * cosine

#                             new_x += origin_x
#                             new_y += origin_y
#                             return [new_x, new_y, 0]

#                         # Move next pointer on node being inserted
#                         # new_node_start, new_node_end = new_node._pointer_to_next.get_start_and_end()
#                         self.node.pointer_to_next.become(
#                             SinglyDirectedEdge(
#                                 start=rotate_start(),
#                                 end=rotate_end()
#                             )
#                         )
#                     flatten_list(self, normalized_alpha)

#     def clean_up_from_scene(self, scene: Scene = None) -> None:
#         scene.add(self.node)
#         self.node.remove(self.sll)
#         scene.remove(self.trav)
#         super().clean_up_from_scene(scene)

#     def _save_state_prev_node_pointer_to_next(self):
#         if self.prev_node_pointer_to_next is not None:
#             self.prev_node_pointer_to_next.save_state()

#     def _restore_prev_node_pointer_to_next(self):
#         if self.prev_node_pointer_to_next is not None:
#             self.prev_node_pointer_to_next.restore()


class Insert(BaseSLLPackager):
    def __init__(self, sll):
        self._sll = sll
        self._trav = Circle().set_opacity(0)

        self._animation_package = AnimationPackage(self._sll)
        self._fade_in_node = None
        self._pointer_animation = None
        self._move_trav = None
        self._center_sll = None
        self._change_next_pointer = None
        self._flatten_list = None
        self._fade_out_temp_trav = None
        self._shift_sub_list = None

    def _assign_subanimations_and_animate(fn):
        def inner(self, *args, **kwargs):
            kwargs.setdefault('display_trav', False)
            kwargs.setdefault('trav_name', 'trav')
            kwargs.setdefault('trav_position', 'start')
            kwargs.setdefault('aligned', False)

            self._animation_package = AnimationPackage(self._sll)
            self._assign_subanimations(*args, **kwargs)
            fn(self, *args, **kwargs)
            # if self._has_non_successive_subanimations():
            self._animation_package.create_ending_subanimation_slls()
            return PackageAnimation(self._sll, self._animation_package)
        return inner
    
    def _has_non_successive_subanimations(self):
        for group in self._animation_package._subanimation_lists:
            if len(group) > 1:
                return True
        return False
    
    def _assign_subanimations(self, index: int, added_node: SLLNode, pointer_animation_type: str, display_trav: bool, trav_name: str, trav_position: str, aligned: bool):
        if aligned:
            added_node.next_to(self._sll[index - 1], RIGHT, buff=0)

        self._fade_in_node = FadeInContainer(self._sll, added_node)
        # FIXME: GrowPointer does a weird movement (though it does end in the correct position)
        self._pointer_animation = self._get_pointer_animation(added_node=added_node, pointer_animation_type=pointer_animation_type)

        if aligned:
            self._shift_sub_list = ShiftSubList(self._sll, index)
            self._center_sll = CenterSLL(self._sll)
            # self._sll[index].pointer_to_next.become(SinglyDirectedEdge(start=self._sll[index].get_container_top(), end=self._sll[index + 1].get_container_bottom()))
        else:
            self._center_sll = CenterSLL(self._sll, restore_sll_at_interpolate=True)

            added_node.container.next_to(self._sll[index + 1].container, DOWN)
            added_node.pointer_to_next.become(SinglyDirectedEdge(start=self._sll[index].get_container_top(), end=self._sll[index + 1].get_container_bottom()))
            self._change_next_pointer = ChangeNextPointer(self._sll, self._sll[index - 1].pointer_to_next, added_node)
            self._flatten_list = FlattenList(self._sll, index, added_node)

        if display_trav:
            trav_starting_node = self._sll[0] if trav_position == 'start' else self._sll[index - 1]
            self._trav = Pointer(trav_starting_node, self._sll, label=trav_name, direction=UP)
            self._animation_package.prepend_successive_animations(
                FadeInTrav(self._sll, self._trav),
                *[
                    MoveTrav(self._sll, self._trav, self._sll[index])
                    for index in range(index)
                ]
            )
        self._fade_out_temp_trav = FadeOutTrav(self._sll, self._trav)

    def _get_pointer_animation(self, added_node: SLLNode, pointer_animation_type: str) -> BaseSubanimation:
        pointer_animation_cls = None
        if pointer_animation_type == 'grow':
            pointer_animation_cls = GrowPointer
        elif pointer_animation_type == 'fade':
            pointer_animation_cls = FadeInPointer
        else:
            raise RuntimeError(f'{pointer_animation_type} not supported for singly linked list node insertion')
        return pointer_animation_cls(self._sll, added_node.pointer_to_next)
    
    @_assign_subanimations_and_animate
    def all_together(
        self,
        index: int,
        data: Any,
        *,
        pointer_animation_type: str,
        **kwargs
    ) -> PackageAnimation:
        self._animation_package.append_concurrent_animations(
            self._fade_in_node,
            self._pointer_animation,
            self._shift_sub_list,
            self._center_sll
        )

    @_assign_subanimations_and_animate
    def insert_test(
        self,
        index: int,
        data: Any,
        *,
        pointer_animation_type: str,
        display_trav: bool,
        trav_name: str,
        trav_position: str,
        **kwargs
    ) -> PackageAnimation:
        self._animation_package.append_concurrent_animations(
            self._fade_in_node,
            self._pointer_animation,
            self._shift_sub_list,
            self._center_sll
            # self._pointer_animation,
            # self._change_next_pointer,
            # self._flatten_list,
            # self._fade_out_temp_trav,
            # self._center_sll
        )