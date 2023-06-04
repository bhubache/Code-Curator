from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from code_curator.automatic_delegation.delegate_to import delegate_to
from colour import Color
from code_curator.constants import DEFAULT_MOBJECT_COLOR
from code_curator.constants import DEFAULT_STROKE_WIDTH
from code_curator.custom_vmobject import CustomVMobject
from manim import Line
from numpy import ndarray

from .weights.edge_weight import EdgeWeight
from .weights.null_weight import NullWeight
from .weights.weight import Weight

DEFAULT_START: ndarray = np.array([-1, 0, 0])
DEFAULT_END: ndarray = np.array([1, 0, 0])


@delegate_to(
    Line,
    to='_line',
    manim_property_include={
        'color',
        'stroke_width',
    },
)
class Edge(CustomVMobject):
    r"""A connection between two :class:`~data_structures.nodes.node.Node`.

    A :class:`~custom_vmobject.CustomVMobject`
    composed of :class:`~manim.manim.mobject.geometry.Line` and :class:`~data_structures.edges.weights.weight.Weight`.

    Args:
        start: The start coordinate.
        end: The end coordinate.
        weight: The associated weight.
        color: The Edge's color.
        line_stroke_width: stroke width of the Edge's line.
    """

    def __init__(
        self,
        start: Sequence[float] | None = None,
        end: Sequence[float] | None = None,
        weight: float | Weight = NullWeight(),
        color: str | Color = DEFAULT_MOBJECT_COLOR,
        line_stroke_width: int = DEFAULT_STROKE_WIDTH,
    ) -> None:
        super().__init__()
        finalized_start: Sequence[float] = start if start is not None else DEFAULT_START
        finalized_end: Sequence[float] = end if end is not None else DEFAULT_END
        self._line: Line = Line(
            start=finalized_start, end=finalized_end, color=color, stroke_width=line_stroke_width,
        )

        if isinstance(weight, float):
            finalized_weight: Weight = EdgeWeight(
                value=weight, color=self.color,
            )
        else:
            finalized_weight = weight

        self._weight: Weight = finalized_weight

        self.add(self._line)
        self.add(self._weight)

    def get_start_and_end(self) -> tuple[Sequence[float], Sequence[float]]:
        return self._line.get_start_and_end()

    @property
    def line(self) -> Line:
        return self._line

    @property
    def weight(self) -> Weight:
        return self._weight

    @property
    def start(self) -> Sequence[float]:
        return self.get_start_and_end()[0]

    @property
    def end(self) -> Sequence[float]:
        return self.get_start_and_end()[1]

    @property
    def vertical_length(self) -> float:
        return abs(self._line.start[1] - self._line.end[1])

    @property
    def horizontal_length(self) -> float:
        return abs(self._line.start[0] - self._line.end[0])

    @property
    def length(self) -> float:
        return self._line.get_length()
