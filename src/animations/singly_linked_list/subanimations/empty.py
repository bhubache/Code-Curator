from __future__ import annotations

from typing import TYPE_CHECKING

from .leaf_subanimation import LeafSubanimation
from src.custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from src.data_structures.singly_linked_list import SinglyLinkedList


class Empty(LeafSubanimation):
    def __init__(self, sll: SinglyLinkedList):
        super().__init__(sll)

    def begin(self) -> None:
        pass

    def interpolate(self, alpha: float) -> None:
        pass

    def clean_up_from_animation(self) -> None:
        pass

    def create_successive_counterpart(self) -> LeafSubanimation:
        return Empty(self._sll)
