from __future__ import annotations

from typing import TYPE_CHECKING

from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.data_structures.nodes.singly_linked_list_node import SLLNode
from code_curator.data_structures.pointers.pointer import Pointer
from manim import smooth

from .leaf_subanimation import LeafSubanimation
from .strictly_successive.move_trav import SuccessiveMoveTrav
# from code_curator.data_structures.edges.singly_directed_edge import SinglyDirectedEdge
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from code_curator.data_structures.singly_linked_list import SinglyLinkedList


class MoveTrav(LeafSubanimation):
    def __init__(self, sll: SinglyLinkedList, trav: Pointer, to_node: SLLNode, run_time: float = 1.0) -> None:
        super().__init__(sll, run_time=run_time)
        self._trav: Pointer = trav
        self._to_node: SLLNode = to_node

    def create_successive_counterpart(self) -> LeafSubanimation:
        return SuccessiveMoveTrav(self._sll, self._trav, self._to_node, run_time=self._run_time)

    def begin(self) -> None:
        self._trav.save_state()

    def interpolate(self, alpha: float) -> None:
        self._trav.restore()
        self._trav.move_immediately_alpha(
            self.finished_subanimation._to_node, self._to_node, smooth(alpha),
        )

    def clean_up_from_animation(self) -> None:
        self._sll.add(self._trav)
        super().clean_up_from_animation()
