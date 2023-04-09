from __future__ import annotations

import numpy as np
from colour import Color
from custom_vmobject import CustomVMobject
from manim import Line
from numpy import ndarray

from ...constants import DEFAULT_MOBJECT_COLOR
from ...constants import DEFAULT_STROKE_WIDTH
from ..null_weight import NullWeight
from ..weight import Weight

DEFAULT_START: ndarray = np.array([-1, 0, 0])
DEFAULT_END: ndarray = np.array([1, 0, 0])


class Edge(CustomVMobject):
    """A connection between two :class:`Node`.

    A :class:`VMobject` composed of :class:`Line` and :class:`Weight`.
    """

    def __init__(
        self,
        start: ndarray | list | None = None,
        end: ndarray | list | None = None,
        weight: float | Weight = NullWeight(),
        line_color: str | Color = DEFAULT_MOBJECT_COLOR,
        line_stroke_width: int = DEFAULT_STROKE_WIDTH,
    ) -> None:
        super().__init__()
        finalized_start: ndarray | list = start if start is not None else DEFAULT_START
        finalized_end: ndarray | list = end if end is not None else DEFAULT_END
        self._line: Line = Line(
            start=finalized_start, end=finalized_end, color=line_color, stroke_width=line_stroke_width,
        )

        finalized_weight: Weight = (
            weight if type(weight) == Weight else
            Weight(
                value=weight, color=self.color,
            )
        )
        self._weight: Weight = finalized_weight

        self.__add_submobjects()

    def __add_submobjects(self) -> None:
        self.add(self._line)

        if self._weight is not None:
            self.add(self._weight)

    def get_start_and_end(self) -> tuple[ndarray, ndarray]:
        return self._line.get_start_and_end()

    @property
    def line(self) -> Line:
        return self._line

    @property
    def weight(self) -> Weight:
        return self._weight

    @property
    def start(self) -> ndarray:
        return self.get_start_and_end()[0]

    @property
    def end(self) -> ndarray:
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
