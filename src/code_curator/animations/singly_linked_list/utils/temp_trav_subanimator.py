from __future__ import annotations

from typing import TYPE_CHECKING

from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.data_structures.nodes.singly_linked_list_node import SLLNode
from code_curator.data_structures.pointers.null_pointer import NullPointer
from code_curator.data_structures.pointers.pointer import Pointer
from manim import UP

from ...subanimation_group import SubanimationGroup
from ..subanimations.fade_in_mobject import FadeInMobject
from ..subanimations.move_trav import MoveTrav
from animations.subanimations.wait import WaitSubanimation
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from code_curator.data_structures.singly_linked_list import SinglyLinkedList


class TempTravSubanimator:
    def __init__(
        self,
        sll: SinglyLinkedList,
        index: int,
        display_first_trav: bool = False,
        first_trav_name: str = 'p1',
        display_second_trav: bool = False,
        second_trav_name: str = 'p2',
        trav_position: str | int = 'start',
        fade_in_temp_trav_timing_info: dict | None = None,
        move_first_temp_trav_timing_info: dict | None = None,
        move_second_temp_trav_timing_info: dict | None = None,
    ) -> None:
        self._sll = sll
        self._index = index
        self._display_first_trav: bool = display_first_trav
        self._first_trav_name: str = first_trav_name
        self._display_second_trav: bool = display_second_trav
        self._second_trav_name: str = second_trav_name
        self._trav_position: str | int = trav_position
        self._first_trav: Pointer = NullPointer()
        self._second_trav: Pointer = NullPointer()

        self._fade_in_temp_trav_timing_info = fade_in_temp_trav_timing_info
        self._move_first_temp_trav_timing_info = move_first_temp_trav_timing_info
        self._move_second_temp_trav_timing_info = move_second_temp_trav_timing_info

        # Start
        self._subanimation_group: SubanimationGroup = self._get_trav_subanimation_group()

    def _get_trav_subanimation_group(self) -> SubanimationGroup:
        if self._display_second_trav and not self._display_first_trav:
            raise Exception(
                'You must also display the first trav to be able to display the second trav',
            )

        if not self._display_first_trav:
            return SubanimationGroup(parent=None)

        self._first_trav = self._create_first_trav()
        self._second_trav = self._create_second_trav()

        first_trav_move_subanimations: SubanimationGroup = self._get_first_trav_move_subanimations()
        second_trav_move_subanimations: SubanimationGroup = self._get_second_trav_move_subanimations()
        combined_subanimations: SubanimationGroup = self._combine_first_and_second_trav_move_subanimations(
            first_trav_moves=first_trav_move_subanimations,
            second_trav_moves=second_trav_move_subanimations,
        )
        trav_subanimation_group: SubanimationGroup = self._prepend_trav_fade_in_subanimations(
            combined_subanimations,
        )

        return trav_subanimation_group

    def _create_first_trav(self) -> Pointer:
        return Pointer(
            self._get_first_trav_starting_node(),
            self._sll,
            label=self._first_trav_name,
            direction=UP,
        ).make_temp()

    def _get_first_trav_starting_node(self) -> SLLNode:
        if self._trav_position == 'start':
            return self._sll[0]
        elif self._trav_position == 'end':
            return self._sll[self._index - 1]
        else:
            return self._sll[self._trav_position]

    def _create_second_trav(self) -> Pointer:
        if not self._display_second_trav:
            return NullPointer()

        return Pointer(
            self._get_second_trav_starting_node(),
            self._sll,
            label=self._second_trav_name,
            direction=UP,
        ).make_temp()

    def _get_second_trav_starting_node(self) -> SLLNode:
        return self._sll[self._get_second_trav_starting_index()]

    def _get_second_trav_starting_index(self) -> int:
        if self._trav_position == 'start':
            return self._get_first_trav_starting_index() + 1
        elif self._trav_position == 'end':
            return self._get_first_trav_starting_index() + 2
        else:
            raise Exception(f'Unexpected trav position {self._trav_position}')

    def _get_first_trav_starting_index(self) -> int:
        return 0 if self._trav_position == 'start' else self._index - 1

    def _get_first_trav_move_subanimations(self) -> SubanimationGroup:
        num_groups = self._index - (self._get_first_trav_starting_index() + 1)
        run_time_per_group = self._move_first_temp_trav_timing_info['run_time'] / num_groups
        return SubanimationGroup(
            *[
                MoveTrav(
                    sll=self._sll, trav=self._first_trav,
                    to_node=self._sll[index],
                    run_time=run_time_per_group,
                )
                for index in range(self._get_first_trav_starting_index() + 1, self._index)
            ],
            lag_ratio=1,
        )

    def _get_second_trav_move_subanimations(self) -> SubanimationGroup:
        if not self._display_second_trav:
            return SubanimationGroup(lag_ratio=1, parent=None)

        num_groups = self._index - (self._get_first_trav_starting_index() + 1)
        run_time_per_group = self._move_first_temp_trav_timing_info['run_time'] / num_groups
        return SubanimationGroup(
            *[
                MoveTrav(
                    sll=self._sll, trav=self._second_trav,
                    to_node=self._sll[index],
                    run_time=run_time_per_group,
                )
                for index in range(self._get_second_trav_starting_index() + 1, self._index + 1)
            ],
            SubanimationGroup(
                MoveTrav(
                    sll=self._sll,
                    trav=self._second_trav,
                    to_node=self._sll[self._index + 1],
                    run_time=self._move_second_temp_trav_timing_info['run_time'],
                )
            ),
            lag_ratio=1,
        )

    def _combine_first_and_second_trav_move_subanimations(
        self,
        first_trav_moves: SubanimationGroup,
        second_trav_moves: SubanimationGroup,
    ) -> SubanimationGroup:
        if not first_trav_moves.contains_subanimations():
            return second_trav_moves
        elif not second_trav_moves.contains_subanimations():
            return first_trav_moves

        combined_moves: SubanimationGroup = SubanimationGroup(lag_ratio=1)
        for i, (first, second) in enumerate(zip(first_trav_moves, second_trav_moves)):
            combined_moves.add(
                SubanimationGroup(first, second, lag_ratio=0, parent=combined_moves, unique_id=f'move_first_temp_trav_{i}'),
            )
        move_second_temp_trav_n: SubanimationGroup = second_trav_moves.get(-1)
        # move_second_temp_trav_n.unique_id = 'move_second_temp_trav_n'
        # move_second_temp_trav_n.parent = combined_moves
        combined_moves.add(move_second_temp_trav_n)
        return combined_moves

    def _prepend_trav_fade_in_subanimations(
        self,
        subanimations: SubanimationGroup,
    ) -> SubanimationGroup:
        run_time = self._fade_in_temp_trav_timing_info['run_time']
        trav_fade_in_subanimations: SubanimationGroup = SubanimationGroup(
            lag_ratio=0,
            unique_id='fade_in_temp_trav',
            parent=subanimations,
        )

        if self._display_first_trav:
            trav_fade_in_subanimations.add(
                FadeInMobject(
                    sll=self._sll, mobject=self._first_trav,
                    parent_mobject=self._sll,
                ),
            )

        if self._display_second_trav:
            trav_fade_in_subanimations.add(
                FadeInMobject(
                    sll=self._sll, mobject=self._second_trav, parent_mobject=self._sll,
                ),
            )

        subanimations.insert(0, trav_fade_in_subanimations)
        subanimations.insert(1, WaitSubanimation(sll=self._sll, run_time=run_time))
        return subanimations

    def has_subanimations(self) -> bool:
        return self._subanimation_group.contains_subanimations()

    def get_subanimation_group(self) -> SubanimationGroup:
        return self._subanimation_group
