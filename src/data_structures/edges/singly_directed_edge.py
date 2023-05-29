from __future__ import annotations

from collections.abc import Sequence

from automatic_delegation.delegate_to import delegate_to
from custom_logging.custom_logger import CustomLogger
from custom_vmobject import CustomVMobject
from data_structures.edges.weights.null_weight import NullWeight
from data_structures.edges.weights.weight import Weight
from manim import CurvedArrow
from manim import VMobject

from .edge import Edge

logger = CustomLogger.getLogger(__name__)


@delegate_to(
    Edge,
    to='_edge',
    manim_property_include={
        'vertical_length',
        'tip',
        'stroke_width',
    },
)
class SinglyDirectedEdge(CustomVMobject):
    def __init__(
        self,
        start: Sequence[float] | None = None,
        end: Sequence[float] | None = None,
        weight: float | Weight = NullWeight(),
        tip_shape: VMobject | None = None,
    ) -> None:
        super().__init__()
        self._edge: Edge = Edge(
            start=start,
            end=end,
            weight=weight,
        )
        self._edge.line.add_tip(
            tip_shape=tip_shape,
            tip_length=0.2,
            tip_width=0.2,
        )
        self.add(self._edge)

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

    @property
    def length(self) -> float:
        return self._edge.length

    def get_start_and_end(self) -> tuple[Sequence[float], Sequence[float]]:
        return self._edge.get_start_and_end()

    @property
    def start(self) -> Sequence[float]:
        return self.get_start_and_end()[0]

    @property
    def end(self) -> Sequence[float]:
        return self.get_start_and_end()[1]
