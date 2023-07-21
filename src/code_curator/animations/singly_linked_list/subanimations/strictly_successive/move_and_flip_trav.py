from __future__ import annotations

import math
from typing import TYPE_CHECKING

import numpy as np
from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.data_structures.nodes.singly_linked_list_node import SLLNode
from code_curator.data_structures.pointers.pointer import Pointer
from code_curator.data_structures.static_array_parts.values.element import Element
from manim import Dot
from manim import Line
from manim import smooth
from numpy import ndarray

from ..leaf_subanimation import LeafSubanimation
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from code_curator.data_structures.singly_linked_list import SinglyLinkedList


class SuccessiveMoveAndFlipTrav(LeafSubanimation):
    def __init__(self, sll: SinglyLinkedList, trav: Pointer, to_node: SLLNode):
        super().__init__(sll)
        self._trav: Pointer = trav
        self._to_node: SLLNode = to_node
        self._trav_end_path: ndarray = None
        self._start_and_end_diff: ndarray = None
        self._trav_label: Element = self._trav.get_label()

    def begin(self) -> None:
        self._trav.save_state()
        trav_final_state = Pointer(
            node=self._to_node,
            sll=self._sll,
            label=self._trav.get_label(),
            direction=self._trav.get_opposite_direction(),
        )
        _, final_state_trav_end = trav_final_state.get_start_and_end()
        initial_state_trav_start, initial_state_trav_end = self._trav.get_start_and_end()
        self._trav_end_path = Line(
            start=initial_state_trav_end, end=final_state_trav_end,
        )

        self._start_and_end_diff = initial_state_trav_end - initial_state_trav_start
        self._trav.move(self._to_node, self._to_node)

    def interpolate(self, alpha: float) -> None:
        self._trav.restore()
        shifted_trav_end: np.ndarray = self._trav_end_path.point_from_proportion(
            smooth(alpha),
        )
        shifted_trav_start: np.ndarray = shifted_trav_end - self._start_and_end_diff

        rotation_angle: float = self._alpha_to_angle(alpha)

        shifted_and_rotated_trav_start = Dot(shifted_trav_start).rotate(
            angle=rotation_angle, about_point=shifted_trav_end,
        ).get_center()

        self._trav.put_start_and_end_on(
            shifted_and_rotated_trav_start, shifted_trav_end,
        )
        self._trav_label.rotate(
            angle=0 - rotation_angle,
            about_point=self._trav_label.get_center(),
        )

    def _alpha_to_angle(self, alpha: float) -> float:
        degrees = (180 * smooth(alpha)) + 0
        return (degrees * math.pi) / 180

    def clean_up_from_animation(self) -> None:
        self._sll.add(self._trav)
        super().clean_up_from_animation()

    # TODO: This method
    def create_successive_counterpart(self) -> LeafSubanimation:
        raise NotImplementedError('')