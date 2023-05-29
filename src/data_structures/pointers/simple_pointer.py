from __future__ import annotations

from collections import Sequence

from custom_logging.custom_logger import CustomLogger
from manim import Mobject

from ..edges.singly_directed_edge import SinglyDirectedEdge
logger = CustomLogger.getLogger(__name__)


class SimplePointer(SinglyDirectedEdge):
    def __init__(
        self,
        start: Sequence[float] | Mobject,
        end: Sequence[float] | Mobject,
    ) -> None:
        super().__init__(start=start, end=end)
