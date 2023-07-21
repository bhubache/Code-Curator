from __future__ import annotations

import math
from typing import TYPE_CHECKING

from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.data_structures.edges.singly_directed_edge import SinglyDirectedEdge
# from code_curator.data_structures.nodes.singly_linked_list_node import SLLNode
from code_curator.data_structures.pointers.pointer import Pointer
from manim import Dot
from manim import Line
from manim import smooth

from .leaf_subanimation import LeafSubanimation
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from code_curator.data_structures.singly_linked_list import SinglyLinkedList


class WavePointer(LeafSubanimation):
    def __init__(
        self,
        sll: SinglyLinkedList,
        pointer: Pointer,
        run_time: float = 1,
        # start_node: SLLNode,
        # new_end_node: SLLNode,
    ) -> None:
        super().__init__(sll, run_time=run_time)
        self._pointer: Pointer = pointer
        # self._start_node: SLLNode = start_node
        # self._new_end_node: SLLNode = new_end_node

    def begin(self) -> None:
        self._sll.add(self._pointer)
        self._pointer.save_state()
        # self._path = Line(start=self._pointer.end, start=self._pointer.start)

    def interpolate(self, alpha: float) -> None:
        self._pointer.restore()
        rotation_angle: float = self._alpha_to_angle(alpha)

        pointer_start, pointer_end = self._pointer.get_start_and_end()
        new_pointer_end = Dot(pointer_end).rotate(
            angle=rotation_angle,
            about_point=pointer_start
        ).get_center()
        self._pointer.put_start_and_end_on(
            pointer_start,
            new_pointer_end,
        )

    def clean_up_from_animation(self) -> None:
        super().clean_up_from_animation()

    # NOTE: This will probably need a different successive counterpart implementation
    def create_successive_counterpart(self) -> LeafSubanimation:
        return WavePointer(
            self._sll,
            self._pointer,
            # self._start_node,
            # self._new_end_node,
        )
    
    # TODO: Remove code duplication
    def _alpha_to_angle(self, alpha: float) -> float:
        degrees = (180 * smooth(alpha)) + 0
        return (degrees * math.pi) / 180
