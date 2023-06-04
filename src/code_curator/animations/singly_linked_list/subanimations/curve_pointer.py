from __future__ import annotations

from typing import TYPE_CHECKING

from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from code_curator.data_structures.nodes.singly_linked_list_node import SLLNode
from code_curator.data_structures.pointers.pointer import Pointer
from manim import Line
from manim import smooth

from .leaf_subanimation import LeafSubanimation
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from code_curator.data_structures.singly_linked_list import SinglyLinkedList


class CurvePointer(LeafSubanimation):
    def __init__(
        self,
        sll: SinglyLinkedList,
        pointer: Pointer,
        start_node: SLLNode,
        new_end_node: SLLNode,
    ) -> None:
        super().__init__(sll)
        self._pointer: Pointer = pointer
        self._start_node: SLLNode = start_node
        self._new_end_node: SLLNode = new_end_node

    def begin(self) -> None:
        self._sll.add(self._pointer)
        # self._path = Line(start=self._pointer.end, start=self._pointer.start)

    def interpolate(self, alpha: float) -> None:
        pointer_start = self._start_node.get_container_right()
        self._path = Line(
            start=self._start_node.next.get_container_left(
            ), end=self._new_end_node.get_container_left(),
        )
        self._pointer.become(
            SinglyDirectedEdge.create_curved_pointer(
                start=pointer_start,
                end=self._path.point_from_proportion(smooth(alpha)),
                angle=(smooth(alpha) * (1.25 + self._start_node.radius)),
            ),
        )

    def clean_up_from_animation(self) -> None:
        super().clean_up_from_animation()

    def create_successive_counterpart(self) -> LeafSubanimation:
        return CurvePointer(self._sll, self._pointer, self._start_node, self._new_end_node)
