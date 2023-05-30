from __future__ import annotations

from typing import TYPE_CHECKING

from custom_logging.custom_logger import CustomLogger
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from data_structures.nodes.singly_linked_list_node import SLLNode
from data_structures.pointers.pointer import Pointer
from data_structures.element import Element
from manim import Line
from manim import smooth
from manim import Transform

from .leaf_subanimation import LeafSubanimation
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from data_structures.singly_linked_list import SinglyLinkedList


class ChangeNodeData(LeafSubanimation):
    def __init__(
        self,
        sll: SinglyLinkedList,
        node: SLLNode,
        new_data,
    ) -> None:
        super().__init__(sll)
        self._node: SLLNode = node
        self._new_data: Element = Element(new_data, font_size=self._node.mobj_data.font_size)
        self._original_state = None

    def begin(self) -> None:
        self._original_state = self._node.mobj_data.copy()
        # self._sll.add(self._pointer)
        # self._path = Line(start=self._pointer.end, start=self._pointer.start)

    def interpolate(self, alpha: float) -> None:
        self._node.mobj_data.become(self._original_state)
        transform = Transform(self._node.mobj_data, self._new_data)
        transform.begin()
        transform.interpolate(smooth(alpha))
        try:
            self._node.mobj_data.move_to(
                [self._node.get_container_center()[0], self._node.next.get_container_center()[1], self._node.get_container_center()[2]]
            )
        except AttributeError:
            raise NotImplementedError('Getting the previous node is not yet implemented')

        # self._node.mobj_data.move_to(self._node.next.container)
        # self._node.mobj_data.move_to(self._node.get_container_center())

    def clean_up_from_animation(self) -> None:
        super().clean_up_from_animation()

    def create_successive_counterpart(self) -> LeafSubanimation:
        return self
