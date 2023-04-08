import numpy as np
from numpy import ndarray

from constants import DEFAULT_STROKE_WIDTH, DEFAULT_MOBJECT_COLOR
from manim import Line, VMobject


class Edge(VMobject):
    def __init__(
        self,
        start: ndarray = None,
        end: ndarray = None,
        color: str = DEFAULT_MOBJECT_COLOR,
        stroke_width: int = DEFAULT_STROKE_WIDTH,
        weight: float = None
    ) -> None:
        super().__init__()
        self._line: Line = Line(start=start, end=end, color=color, stroke_width=stroke_width)
        self._weight: float = weight

        self.add(self._line)

    def get_start_and_end(self):
        return self._line.get_start_and_end()

    @property
    def start(self) -> np.ndarray:
        return self.get_start_and_end()[0]

    @property
    def end(self) -> np.ndarray:
        return self.get_start_and_end()[1]

    # FIXME: This is just for vertical edges
    @property
    def vertical_length(self):
        return abs(self._line.start[1] - self._line.end[1])

    @property
    def horizontal_length(self):
        return abs(self._line.start[0] - self._line.end[0])

    @property
    def length(self):
        return self._line.get_length()
