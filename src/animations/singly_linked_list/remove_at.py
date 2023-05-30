from __future__ import annotations

from typing import Any
from typing import TYPE_CHECKING

from custom_logging.custom_logger import CustomLogger
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from data_structures.nodes.singly_linked_list_node import SLLNode
from data_structures.pointers.pointer import Pointer
from manim import VGroup

from .data_structure_animator import _register_subanimation
from .data_structure_animator import DataStructureAnimator
from .subanimations.base_subanimation import BaseSubanimation
from .subanimations.center_sll import CenterSLL
from .subanimations.curve_pointer import CurvePointer
from .subanimations.empty import Empty
from .subanimations.fade_out_container import FadeOutContainer
from .subanimations.fade_out_mobject import FadeOutMobject
from .subanimations.flatten_list_for_remove import FlattenListForRemove
from .subanimations.shrink_pointer import ShrinkPointer
from .subanimations.unshrink_pointer import UnshrinkPointer
from .utils.temp_trav_subanimator import TempTravSubanimator
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from data_structures.singly_linked_list import SinglyLinkedList


class RemoveAt(DataStructureAnimator):
    def __init__(
        self,
        sll: SinglyLinkedList,
        index: int,
        node: SLLNode,
        display_first_trav: bool,
        first_trav_name: str,
        display_second_trav: bool,
        second_trav_name: str,
        trav_position: str,
        aligned: bool,
        **kwargs: Any,
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
            **kwargs,
        )
        self._removed_node_index: int = index
        self._removed_node: SLLNode = node
        self._display_first_trav: bool = display_first_trav
        self._first_trav_name: str = first_trav_name
        self._display_second_trav: bool = display_second_trav
        self._second_trav_name: str = second_trav_name
        self._trav_position: str = trav_position
        self._aligned: bool = aligned

        self._prev_node: SLLNode = self._sll[self._removed_node_index - 1]
        self._prev_node_pointer: SinglyDirectedEdge = self._prev_node.pointer_to_next
        self._next_node: SLLNode = self._sll[self._removed_node_index + 1]

        self._first_trav: Pointer | None = None
        self._second_trav: Pointer | None = None

        self._build_animation()

    @staticmethod
    def create_packager(
        sll: SinglyLinkedList,
        index: int,
        node: SLLNode,
        display_first_trav: bool,
        first_trav_name: str,
        display_second_trav: bool,
        second_trav_name: str,
        trav_position: str,
        aligned: bool,
        **kwargs: Any,
    ) -> RemoveAt:
        return RemoveAt(
            sll=sll,
            index=index,
            node=node,
            display_first_trav=display_first_trav,
            first_trav_name=first_trav_name,
            display_second_trav=display_second_trav,
            second_trav_name=second_trav_name,
            trav_position=trav_position,
            aligned=aligned,
            **kwargs,
        )

    @_register_subanimation
    def with_fade_out_container(self) -> DataStructureAnimator:
        return self._add_subanimation_concurrently(self._create_fade_out_container())

    @_register_subanimation
    def subsequently_fade_out_container(self) -> DataStructureAnimator:
        return self._add_subanimation_successively(self._create_fade_out_container())

    @_register_subanimation
    def with_fade_out_pointer(self) -> DataStructureAnimator:
        return self._add_subanimation_concurrently(self._create_fade_out_pointer())

    @_register_subanimation
    def subsequently_fade_out_pointer(self) -> DataStructureAnimator:
        return self._add_subanimation_successively(self._create_fade_out_pointer())

    @_register_subanimation
    def with_shrink_pointer(self) -> DataStructureAnimator:
        return self._add_subanimation_concurrently(self._create_shrink_pointer())

    @_register_subanimation
    def subsequently_shrink_pointer(self) -> DataStructureAnimator:
        return self._add_subanimation_successively(self._create_shrink_pointer())

    @_register_subanimation
    def with_unshrink_pointer(self) -> DataStructureAnimator:
        return self._add_subanimation_concurrently(self._create_unshrink_pointer())

    @_register_subanimation
    def subsequently_unshrink_pointer(self) -> DataStructureAnimator:
        return self._add_subanimation_successively(self._create_unshrink_pointer())

    @_register_subanimation
    def with_curve_pointer(self) -> DataStructureAnimator:
        return self._add_subanimation_concurrently(self._create_curve_pointer())

    @_register_subanimation
    def subsequently_curve_pointer(self) -> DataStructureAnimator:
        return self._add_subanimation_successively(self._create_curve_pointer())

    @_register_subanimation
    def with_center_sll(self) -> DataStructureAnimator:
        return self._add_subanimation_concurrently(self._create_center_sll())

    @_register_subanimation
    def subsequently_center_sll(self) -> DataStructureAnimator:
        return self._add_subanimation_successively(self._create_center_sll())

    @_register_subanimation
    def with_flatten_list(self) -> DataStructureAnimator:
        return self._add_subanimation_concurrently(self._create_flatten_list())

    @_register_subanimation
    def subsequently_flatten_list(self) -> DataStructureAnimator:
        return self._add_subanimation_successively(self._create_flatten_list())

    @_register_subanimation
    def with_fade_out_first_temp_trav(self) -> DataStructureAnimator:
        return self._add_subanimation_concurrently(self._create_fade_out_first_temp_trav())

    @_register_subanimation
    def subsequently_fade_out_first_temp_trav(self) -> DataStructureAnimator:
        return self._add_subanimation_successively(self._create_fade_out_first_temp_trav())

    @_register_subanimation
    def with_fade_out_second_temp_trav(self) -> DataStructureAnimator:
        return self._add_subanimation_concurrently(self._create_fade_out_second_temp_trav())

    @_register_subanimation
    def subsequently_fade_out_second_temp_trav(self) -> DataStructureAnimator:
        return self._add_subanimation_successively(self._create_fade_out_second_temp_trav())

    # TODO: Give a more descriptive name
    def _build_animation(self) -> None:
        self._include_trav_subanimations()

    def _include_trav_subanimations(self) -> None:
        temp_trav_subanimator = TempTravSubanimator(
            sll=self._sll,
            index=self._removed_node_index,
            display_first_trav=self._display_first_trav,
            first_trav_name=self._first_trav_name,
            display_second_trav=self._display_second_trav,
            second_trav_name=self._second_trav_name,
            trav_position=self._trav_position,
        )
        if temp_trav_subanimator.has_subanimations():
            self._prepend_subanimation(
                temp_trav_subanimator.get_subanimation_group(),
            )

        # TODO: Find a better place and/or higher level of abstraction
        self._first_trav = temp_trav_subanimator._first_trav
        self._second_trav = temp_trav_subanimator._second_trav

    def clean_up_mobject(self) -> None:
        del self._sll._nodes[self._removed_node_index]

    def _get_sll_to_forecast(self) -> SinglyLinkedList:
        sll_to_forecast = self._sll.copy()
        return sll_to_forecast

    def _create_fade_out_container(self) -> BaseSubanimation:
        return FadeOutContainer(
            sll=self._sll,
            container=self._removed_node.container,
            node=self._removed_node,
        )

    def _create_fade_out_pointer(self) -> BaseSubanimation:
        return FadeOutMobject(
            sll=self._sll,
            mobject=self._removed_node.pointer_to_next,
            parent_mobject=self._removed_node,
        )

    def _create_shrink_pointer(self) -> BaseSubanimation:
        return ShrinkPointer(
            sll=self._sll,
            pointer=self._prev_node_pointer,
            node=self._prev_node,
        )

    def _create_unshrink_pointer(self) -> BaseSubanimation:
        return UnshrinkPointer(
            sll=self._sll,
            pointer=self._prev_node_pointer,
            node=self._prev_node,
        )

    def _create_curve_pointer(self) -> BaseSubanimation:
        return CurvePointer(
            sll=self._sll,
            pointer=self._prev_node_pointer,
            start_node=self._prev_node,
            new_end_node=self._next_node,
        )

    def _create_center_sll(self) -> BaseSubanimation:
        return CenterSLL(
            sll=self._sll,
            curr_reference_index=self._removed_node_index + 1,
            post_subanimation_reference_index=self._removed_node_index,
        )

    def _create_flatten_list(self) -> BaseSubanimation:
        sub_list_to_shift = VGroup(
            *[
                node for i, node in enumerate(
                    self._sll,
                ) if i > self._removed_node_index
            ], self._sll.tail_pointer,
        )
        if self._display_second_trav and self._second_trav in self._sll.submobjects:
            sub_list_to_shift.add(self._second_trav)

        return FlattenListForRemove(
            sll=self._sll,
            start_node=self._prev_node,
            end_node=self._next_node,
            pointer_to_straighten=self._prev_node_pointer,
            sub_list_to_shift=sub_list_to_shift,
        )

    def _create_fade_out_first_temp_trav(self) -> BaseSubanimation:
        if not self._display_first_trav:
            return Empty(self._sll)

        return FadeOutMobject(
            sll=self._sll,
            mobject=self._first_trav,
            parent_mobject=self._sll,
        )

    def _create_fade_out_second_temp_trav(self) -> BaseSubanimation:
        if not self._display_second_trav:
            return Empty(self._sll)

        return FadeOutMobject(
            sll=self._sll,
            mobject=self._second_trav,
            parent_mobject=self._sll,
        )
