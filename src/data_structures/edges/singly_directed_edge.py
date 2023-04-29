from __future__ import annotations

from collections.abc import Sequence

from manim import CurvedArrow
from manim import VMobject

from .edge import Edge
from src.custom_logging.custom_logger import CustomLogger
from src.custom_vmobject import CustomVMobject
from src.data_structures.edges.weights.null_weight import NullWeight
from src.data_structures.edges.weights.weight import Weight

logger = CustomLogger.getLogger(__name__)


class SinglyDirectedEdge(CustomVMobject):
    def __init__(
        self,
        start: Sequence[float] | None = None,
        end: Sequence[float] | None = None,
        weight: float | Weight = NullWeight(),
        tip_shape: VMobject | None = None,
    ) -> None:
        self._edge: Edge = Edge(
            start=start,
            end=end,
            weight=weight,
        )
        self._add_tip(tip_shape=tip_shape, tip_length=0.2, tip_width=0.2)
        self.add(self._edge)

    def _add_tip(self, tip_shape: VMobject, tip_length: float, tip_width: float) -> None:
        self._edge.line.add_tip(
            tip_shape=tip_shape,
            tip_length=tip_length,
            tip_width=tip_width,
        )

    def create_curved_pointer(start: Sequence[float], end: Sequence[float], **kwargs) -> CurvedArrow:
        singly_directed_edge = SinglyDirectedEdge(0, 1)
        curved_pointer = CurvedArrow(
            start,
            end,
            tip_length=singly_directed_edge.tip.length,
            **kwargs,
        )
        curved_pointer.set_color('#DBC9B8')
        curved_pointer.set_stroke_width(singly_directed_edge.stroke_width)

        return curved_pointer
