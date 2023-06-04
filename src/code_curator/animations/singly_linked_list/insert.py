from __future__ import annotations
from typing import Any
import math

from .data_structure_animator import BaseSLLPackager, assign_subanimations_and_animate
from data_structures import singly_linked_list
from animations.singly_linked_list.add_first import AddFirst
from data_structures.nodes.singly_linked_list_node import SLLNode
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from data_structures.pointers.pointer import Pointer
from .subanimations.base_subanimation import BaseSubanimation
from ..animation_package import AnimationPackage
from ..data_structure_animation import PackageAnimation
from .subanimations.fade_in_container import FadeInContainer
from .subanimations.fade_in_mobject import FadeInMobject
from .subanimations.fade_out_mobject import FadeOutMobject
# from .subanimations.fade_in_pointer import FadeInPointer
from .subanimations.grow_pointer import GrowPointer
from .subanimations.move_trav import MoveTrav
from .subanimations.center_sll import CenterSLL
from .subanimations.change_next_pointer import ChangeNextPointer
from .subanimations.flatten_list import FlattenList
# from .subanimations.fade_in_trav import FadeInTrav
# from .subanimations.fade_out_trav import FadeOutTrav
from .subanimations.shift_sub_list import ShiftSubList
from .subanimations.strictly_successive.shift_sub_list import SuccessiveShiftSubList
from .subanimations.strictly_successive.center_sll import SuccessiveCenterSLL
from .subanimations.empty import Empty
from .utils.temp_trav_subanimator import TempTravSubanimator
from manim import Animation, linear, smooth, Scene, LEFT, UP, DOWN, RIGHT, VGroup, Circle

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)


class Insert(BaseSLLPackager):
    def __init__(
        self,
        sll,
        index: int,
        node: SLLNode,
        display_first_trav: bool,
        first_trav_name: str,
        display_second_trav: bool,
        second_trav_name: str,
        trav_position: str,
        aligned: bool,
        **kwargs
    ) -> None:
        super().__init__(
            sll=sll,
            index=index,
            node=node,
            display_first_trav=display_first_trav,
            first_trav_name=first_trav_name,
            display_second_trav=display_second_trav,
            second_trav_name=second_trav_name,
            trav_position=trav_position,
            aligned=aligned,
            **kwargs
        )
        self._inserted_node_index: int = index
        self._inserted_node: SLLNode = node
        self._display_first_trav: bool = display_first_trav
        self._first_trav_name: str = first_trav_name
        self._display_second_trav: bool = display_second_trav
        self._second_trav_name: str = second_trav_name
        self._trav_position: str = trav_position
        self._aligned: bool = aligned

        self._prev_node_pointer: SinglyDirectedEdge = self._sll[self._inserted_node_index - 1].pointer_to_next

        self._build_animation()

        ############################################################################################
        ############################################################################################
        ############################################################################################

        # self._trav = Circle().set_opacity(0)

        # self._fade_in_container = Empty(self._sll)
        # self._pointer_animation = Empty(self._sll)
        # # self._move_trav = Empty(self._sll)
        # self._center_sll = Empty(self._sll)
        # self._change_next_pointer = Empty(self._sll)
        # self._flatten_list = Empty(self._sll)
        # self._fade_out_temp_trav = Empty(self._sll)
        # self._shift_sub_list = Empty(self._sll)
        # self._move_head_trav = Empty(self._sll)

    @staticmethod
    def create_packager(
        sll,
        index: int,
        node: SLLNode,
        display_first_trav: bool,
        first_trav_name: str,
        display_second_trav: bool,
        second_trav_name: str,
        trav_position: str,
        aligned: bool,
        **kwargs
    ) -> Insert:
        return Insert(
            sll=sll,
            index=index,
            node=node,
            display_first_trav=display_first_trav,
            first_trav_name=first_trav_name,
            display_second_trav=display_second_trav,
            second_trav_name=second_trav_name,
            trav_position=trav_position,
            aligned=aligned,
            **kwargs
        )

    # TODO: Give a more descriptive name
    def _build_animation(self):
        self._include_trav_subanimations()

    def _include_trav_subanimations(self):
        temp_trav_subanimator = TempTravSubanimator(
            sll=self._sll,
            index=self._inserted_node_index,
            display_first_trav=self._display_first_trav,
            first_trav_name=self._first_trav_name,
            display_second_trav=self._display_second_trav,
            second_trav_name=self._second_trav_name,
            trav_position=self._trav_position
        )
        if temp_trav_subanimator.has_subanimations():
            self._prepend_subanimation_groups(temp_trav_subanimator.get_subanimation_groups())

        # TODO: Find a better place and/or higher level of abstraction
        self._first_trav = temp_trav_subanimator._first_trav
        self._second_trav = temp_trav_subanimator._second_trav

    def clean_up_mobject(self) -> None:
        self._sll.add(self._inserted_node)
        self._sll.remove(self._inserted_node.container)
        self._sll.remove(self._inserted_node.pointer_to_next)

    def _create_fade_in_container(self) -> BaseSubanimation:
        return FadeInContainer(
            sll=self._sll,
            container=self._inserted_node.container,
            node=self._inserted_node
        )

    def _create_fade_in_pointer(self) -> BaseSubanimation:
        return FadeInMobject(
            sll=self._sll,
            mobject=self._inserted_node.pointer_to_next,
            parent_mobject=self._inserted_node
        )

    def _create_change_prev_node_pointer(self) -> BaseSubanimation:
        return ChangeNextPointer(
            sll=self._sll,
            pointer=self._prev_node_pointer,
            node_to_be_attached=self._inserted_node
        )

    def _create_shift_sub_list(self) -> BaseSubanimation:
        return ShiftSubList(
            sll=self._sll,
            sub_list_to_shift=VGroup(*[node for i, node in enumerate(self._sll) if i > self._inserted_node_index], self._sll.tail_pointer),
            index=self._inserted_node_index
        )

    def _create_flatten_list(self) -> BaseSubanimation:
        return FlattenList(
            sll=self._sll,
            index=self._inserted_node_index,
            added_node=self._inserted_node
        )

    def _create_center_sll(self) -> BaseSubanimation:
        return CenterSLL(
            self._sll,
            curr_reference_index=self._inserted_node_index,
            post_subanimation_reference_index=self._inserted_node_index - 1
        )

    # TODO: Remove duplicate code RemoveAt
    def _create_fade_out_first_temp_trav(self) -> BaseSubanimation:
        if not self._display_first_trav:
            return Empty(self._sll)

        return FadeOutMobject(
            sll=self._sll,
            mobject=self._first_trav,
            parent_mobject=self._sll
        )

    # def _assign_subanimations(self, index: int, node: SLLNode, pointer_animation_type: str, display_trav: bool, trav_name: str, trav_position: str, aligned: bool):
    #     # if index == 0:
    #     #     self._move_head_trav = MoveTrav(self._sll, self._sll.head_pointer, node)
    #     self._fade_in_container = FadeInContainer(self._sll, node.container)

    #     # TODO: Make this standardized
    #     node.container.set_opacity(0)
    #     node.pointer_to_next.set_opacity(0)
    #     # FIXME: GrowPointer does a weird movement (though it does end in the correct position)
    #     self._pointer_animation = self._get_pointer_animation(node=node, pointer_animation_type=pointer_animation_type)

    #     if aligned:
    #         self._shift_sub_list = ShiftSubList(self._sll, VGroup(*[node for i, node in enumerate(self._sll) if i > index], self._sll.tail_pointer), index)
    #         self._center_sll = CenterSLL(self._sll)
    #         # self._sll[index].pointer_to_next.become(SinglyDirectedEdge(start=self._sll[index].get_container_top(), end=self._sll[index + 1].get_container_bottom()))
    #     else:
    #         self._center_sll = CenterSLL(self._sll)

    #         # node.container.next_to(self._sll[index + 1].container, DOWN)
    #         # node.pointer_to_next.become(SinglyDirectedEdge(start=self._sll[index].get_container_top(), end=self._sll[index + 1].get_container_bottom()))
    #         self._change_next_pointer = ChangeNextPointer(self._sll, self._sll[index - 1].pointer_to_next, node)
    #         self._flatten_list = FlattenList(self._sll, index, node)

    #     if display_trav:
    #         trav_starting_node, trav_starting_index = (self._sll[0], 0) if trav_position == 'start' else (self._sll[index - 1], index - 1)
    #         self._trav = Pointer(trav_starting_node, self._sll, label=trav_name, direction=UP)
    #         self._animation_package.prepend_successive_animations(
    #             FadeInMobject(self._sll, self._trav),
    #             *[
    #                 MoveTrav(self._sll, self._trav, self._sll[i])
    #                 for i in range(trav_starting_index + 1, index)
    #             ]
    #         )
    #         self._fade_out_temp_trav = FadeOutMobject(self._sll, self._trav, self._sll)
