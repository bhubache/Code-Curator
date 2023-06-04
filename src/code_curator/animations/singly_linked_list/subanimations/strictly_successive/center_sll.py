from __future__ import annotations

from typing import TYPE_CHECKING

from code_curator.custom_logging.custom_logger import CustomLogger
from manim import Line
from manim import smooth

from ..leaf_subanimation import LeafSubanimation
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from code_curator.data_structures.singly_linked_list import SinglyLinkedList


class SuccessiveCenterSLL(LeafSubanimation):
    def __init__(self, sll: SinglyLinkedList):
        super().__init__(sll)

    def begin(self):
        begin_center = self._sll.get_center()
        # TODO: Change hardcoded origin to dynamic origin
        self._sll_path = Line(start=begin_center, end=[0, 0, 0])

    def interpolate(self, alpha: float):
        self._sll.move_to(self._sll_path.point_from_proportion(smooth(alpha)))

    def clean_up_from_animation(self):
        super().clean_up_from_animation()

    def create_successive_counterpart(self) -> LeafSubanimation:
        return SuccessiveCenterSLL(self._sll)
