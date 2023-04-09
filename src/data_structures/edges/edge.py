from __future__ import annotations

import numpy as np
from colour import Color
from manim import Line
from manim import VMobject
from numpy import ndarray

from ...constants import DEFAULT_MOBJECT_COLOR
from ...constants import DEFAULT_STROKE_WIDTH


class Edge(VMobject):
    def __init__(
        self,
        start: ndarray | list | None = None,
        end: ndarray | list | None = None,
        line_color: str | Color = DEFAULT_MOBJECT_COLOR,
        line_stroke_width: int = DEFAULT_STROKE_WIDTH,
        weight: float | None = None,
    ) -> None:
        super().__init__()
        if start is None:
            start = np.array([-1, 0, 0])
        if end is None:
            end = np.array([1, 0, 0])

        self._line: Line = Line(
            start=start, end=end, color=line_color, stroke_width=line_stroke_width,
        )
        self._weight: float | None = weight

        self.add(self._line)

    def get_start_and_end(self) -> tuple[ndarray, ndarray]:
        return self._line.get_start_and_end()

    @property
    def start(self) -> ndarray:
        return self.get_start_and_end()[0]

    @property
    def end(self) -> ndarray:
        return self.get_start_and_end()[1]

    @property
    def line(self) -> Line:
        return self._line

    @property
    def weight(self) -> float | None:
        return self._weight

    @property
    def vertical_length(self) -> float:
        return abs(self._line.start[1] - self._line.end[1])

    @property
    def horizontal_length(self) -> float:
        return abs(self._line.start[0] - self._line.end[0])

    @property
    def length(self) -> float:
        return self._line.get_length()
