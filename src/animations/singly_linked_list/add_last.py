from __future__ import annotations

from typing import Any
from typing import TYPE_CHECKING

from ..singly_linked_list.subanimations.center_sll import CenterSLL
from ..singly_linked_list.subanimations.fade_in_container import FadeInContainer
from ..singly_linked_list.subanimations.fade_in_mobject import FadeInMobject
from ..singly_linked_list.subanimations.flatten_tail import FlattenTail
from ..singly_linked_list.subanimations.move_and_flip_trav import MoveAndFlipTrav
from ..singly_linked_list.subanimations.move_trav import MoveTrav
from .data_structure_animator import _register_subanimation
from .data_structure_animator import DataStructureAnimator
from .subanimations.leaf_subanimation import LeafSubanimation
from .utils.temp_trav_subanimator import TempTravSubanimator
from src.custom_logging.custom_logger import CustomLogger
from src.data_structures import singly_linked_list
from src.data_structures.nodes.singly_linked_list_node import SLLNode
from src.data_structures.pointers.pointer import Pointer
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from src.data_structures.singly_linked_list import SinglyLinkedList


class AddLast(DataStructureAnimator):
    def __init__(
        self,
        sll: SinglyLinkedList,
        index: int,
        node: SLLNode,
        display_first_trav: bool,
        first_trav_name: str,
        trav_position: str,
        aligned: bool,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            sll=sll,
            index=index,
            data=node.data,
            node=node,
            display_first_trav=display_first_trav,
            first_trav_name=first_trav_name,
            trav_position=trav_position,
            aligned=aligned,
            **kwargs,
        )
        self._added_node_index: int = index
        self._added_node: SLLNode = node
        self._display_first_trav: bool = display_first_trav
        self._first_trav_name: str = first_trav_name
        self._trav_position: str = trav_position
        self._aligned: bool = aligned

        # self._prev_node: SLLNode = self._sll[self._added_node_index - 1]
        # self._prev_node_pointer: SinglyDirectedEdge = self._prev_node.pointer_to_next
        # self._next_node: SLLNode = self._sll[self._added_node_index + 1]

        self._first_trav: Pointer | None = None
        # self._second_trav: Pointer = None

        self._build_animation()

    @staticmethod
    def create_packager(
        sll: SinglyLinkedList,
        index: int,
        node: SLLNode,
        display_first_trav: bool,
        first_trav_name: str,
        trav_position: str,
        aligned: bool,
        **kwargs: Any,
    ) -> AddLast:
        return AddLast(
            sll=sll,
            index=index,
            node=node,
            display_first_trav=display_first_trav,
            first_trav_name=first_trav_name,
            trav_position=trav_position,
            aligned=aligned,
            **kwargs,
        )

    @_register_subanimation
    def with_center_sll(self) -> DataStructureAnimator:
        return self._add_subanimation_concurrently(self._create_center_sll())

    @_register_subanimation
    def subsequently_center_sll(self) -> DataStructureAnimator:
        return self._add_subanimation_successively(self._create_center_sll())

    @_register_subanimation
    def with_fade_in_container(self) -> DataStructureAnimator:
        return self._add_subanimation_concurrently(self._create_fade_in_container())

    @_register_subanimation
    def subsequently_fade_in_container(self) -> DataStructureAnimator:
        return self._add_subanimation_successively(self._create_fade_in_container())

    @_register_subanimation
    def with_fade_in_pointer(self) -> DataStructureAnimator:
        return self._add_subanimation_concurrently(self._create_fade_in_pointer())

    @_register_subanimation
    def subsequently_fade_in_pointer(self) -> DataStructureAnimator:
        return self._add_subanimation_successively(self._create_fade_in_pointer())

    @_register_subanimation
    def with_move_tail(self) -> DataStructureAnimator:
        return self._add_subanimation_concurrently(self._create_move_tail())

    @_register_subanimation
    def subsequently_move_tail(self) -> DataStructureAnimator:
        return self._add_subanimation_successively(self._create_move_tail())

    # TODO: Give a more descriptive name
    def _build_animation(self) -> None:
        self._include_trav_subanimations()

    def _include_trav_subanimations(self) -> None:
        temp_trav_subanimator = TempTravSubanimator(
            sll=self._sll,
            index=self._added_node_index,
            display_first_trav=self._display_first_trav,
            first_trav_name=self._first_trav_name,
            display_second_trav=False,
            trav_position=self._trav_position,
        )
        if temp_trav_subanimator.has_subanimations():
            self._prepend_subanimation(
                temp_trav_subanimator.get_subanimation_group(),
            )

        # TODO: Find a better place and/or higher level of abstraction
        self._first_trav = temp_trav_subanimator._first_trav
        # self._second_trav = temp_trav_subanimator._second_trav

    # FIXME: Remove node graphically and shift sub list!!!
    def _get_sll_to_forecast(self) -> SinglyLinkedList:
        sll_to_forecast = self._sll.copy()
        del sll_to_forecast[self._added_node_index]
        return singly_linked_list.SinglyLinkedList.create_sll(sll_to_forecast)

        # return sll_to_forecast

    def clean_up_mobject(self) -> None:
        del self._sll._nodes[self._added_node_index]

    def _create_fade_in_container(self) -> LeafSubanimation:
        return FadeInContainer(
            sll=self._sll,
            container=self._added_node.container,
            node=self._added_node,
        )

    def _create_fade_in_pointer(self) -> LeafSubanimation:
        return FadeInMobject(
            sll=self._sll,
            mobject=self._sll[self._added_node_index - 1].pointer_to_next,
            parent_mobject=self._sll[self._added_node_index - 1],
        )

    def _create_center_sll(self) -> LeafSubanimation:
        return CenterSLL(
            sll=self._sll,
            curr_reference_index=1,
            post_subanimation_reference_index=0,
        )

    def _create_flatten_tail(self) -> LeafSubanimation:
        return FlattenTail(
            sll=self._sll,
            index=self._added_node_index,
            added_node=self._added_node,
        )

    def _create_move_tail(self) -> LeafSubanimation:
        move_trav_cls: type[LeafSubanimation] | None = None
        if self._sll_went_from_one_to_two_nodes():
            move_trav_cls = MoveAndFlipTrav
        else:
            move_trav_cls = MoveTrav

        return move_trav_cls(
            sll=self._sll,
            trav=self._sll.tail_pointer,
            to_node=self._added_node,
        )
        # return move_trav_cls(
        #     sll=self._sll,
        #     trav=self._sll.tail_pointer,
        #     to_node=self._added_node,
        # )

    def _sll_went_from_one_to_two_nodes(self) -> bool:
        return len(self._sll) == 2
