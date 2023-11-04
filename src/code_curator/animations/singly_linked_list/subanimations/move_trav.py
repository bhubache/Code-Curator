from __future__ import annotations

from typing import TYPE_CHECKING

from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.data_structures.nodes.node import Node
from code_curator.data_structures.pointers.pointer import Pointer
from manim import Line
from manim import smooth
from manim import Circle

from .leaf_subanimation import LeafSubanimation
from .strictly_successive.move_trav import SuccessiveMoveTrav
# from code_curator.data_structures.edges.singly_directed_edge import SinglyDirectedEdge
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from code_curator.data_structures.singly_linked_list import SinglyLinkedList


class MoveTrav(LeafSubanimation):
    def __init__(self, sll: SinglyLinkedList, trav: Pointer, to_node: Node, run_time: float = 1.0) -> None:
        super().__init__(sll, run_time=run_time)
        self._trav: Pointer = trav
        self._to_node: Node = to_node
        self.path = Line(
            start=self._trav.get_start_and_end()[1],
            end=self._trav._relative_placement(self._to_node),
        )

    def create_successive_counterpart(self) -> LeafSubanimation:
        return SuccessiveMoveTrav(self._sll, self._trav, self._to_node, run_time=self._run_time)

    def begin(self) -> None:
        self._trav.save_state()

    def interpolate(self, alpha: float) -> None:
        self._trav.restore()

        new_end = self.path.point_from_proportion(smooth(alpha))
        self._trav.put_start_and_end_on(
            start=new_end + (self._trav.start - self._trav.end),
            end=new_end,
        )

    def clean_up_from_animation(self) -> None:
        self._sll.add(self._trav)
        self._trav.remove(self._trav.node)
        self._to_node.add_incoming_arrow(self._trav)
        super().clean_up_from_animation()
