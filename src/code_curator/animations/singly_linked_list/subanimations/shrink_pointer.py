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


class ShrinkPointer(LeafSubanimation):
    def __init__(
        self,
        sll: SinglyLinkedList,
        pointer: Pointer,
        node: SLLNode,
        run_time: float = 1.0,
    ) -> None:
        super().__init__(sll, run_time=run_time)
        self._pointer: Pointer = pointer
        self._node: SLLNode = node

    def begin(self) -> None:
        self._sll.add(self._pointer)
        # self._path = Line(start=self._pointer.end, start=self._pointer.start)

    def interpolate(self, alpha: float) -> None:
        pointer_start = self._node.get_container_right()
        self._path = Line(
            start=pointer_start,
            end=self._node.next.get_container_left(),
        )
        tip_length = self._pointer.tip.length
        self._pointer.become(
            SinglyDirectedEdge(
                start=pointer_start,
                end=self._path.point_from_proportion(
                    1 - smooth(alpha),
                ) + [tip_length * smooth(alpha), 0, 0],
            ),
        )

    def clean_up_from_animation(self) -> None:
        super().clean_up_from_animation()

    def create_successive_counterpart(self) -> LeafSubanimation:
        return ShrinkPointer(self._sll, self._pointer, self._node)
