from __future__ import annotations

import math
from typing import TYPE_CHECKING

from manim import BLACK
from manim import Circle
from manim import Line
from manim import Mobject

from code_curator.constants import DEFAULT_ELEMENT_FONT_SIZE
from code_curator.custom_vmobject import CustomVMobject
from code_curator.data_structures.element import Element

if TYPE_CHECKING:
    from colour import Color


class Vertex(CustomVMobject):
    def __init__(
        self,
        label: str | Mobject,
        /,
        *,
        contents: str | Mobject | None = None,
        container: Mobject | None = None,
        position: tuple[float, float, float] = (0.0, 0.0, 0.0),
        label_out: bool = False,
        label_dist: float = 0.0,
        label_revolve_angle_in_degrees: float = 0.0,
        label_rotate_angle_in_degrees: float = 0.0,
        show_label: bool = True,
    ) -> None:
        super().__init__()
        if not isinstance(label, Mobject):
            label = Element(label, color=BLACK, font_size=DEFAULT_ELEMENT_FONT_SIZE - 2)

        if container is None:
            container = Circle(color=BLACK, radius=0.2, stroke_width=0.75)

        if label_out:
            circumscribing_circle = Circle(stroke_width=0.75).surround(
                container,
                buffer_factor=1 + label_dist,
            )
            label.move_to(
                circumscribing_circle.point_at_angle(
                    math.radians(label_revolve_angle_in_degrees),
                ),
            )

        self.label = label
        self.container = container
        self.contents = contents

        if self.contents is not None:
            self.contents = Element(
                contents,
                color=BLACK,
                font_size=DEFAULT_ELEMENT_FONT_SIZE - 2,
            )
            self.container.add(self.contents)

        self.container.add(label)
        self.container.move_to(position)

        self.add(container)

    def label_is(self, value: str) -> bool:
        return self.label.value == value


class Graph(CustomVMobject):
    def __init__(self) -> None:
        super().__init__()
        self.vertices: list[Vertex] = []

    def add_vertex(
        self,
        label_or_vertex: str | Vertex,
        **kwargs,
    ) -> None:
        if not isinstance(label_or_vertex, Vertex):
            label_or_vertex = Vertex(label_or_vertex, **kwargs)

        self.add(label_or_vertex)
        self.vertices.append(label_or_vertex)

    def add_edge(
        self,
        vertex_one: str | Mobject,
        vertex_two: str | Mobject,
        *,
        label: str | None = None,
        color: str | Color = BLACK,
        opacity: float = 1.0,
        line_stroke_width: float = 1.0,
        label_distance_proportion: float = 0.5,
        label_line_sep: float = 0.1,
        label_container: Mobject | None = None,
        label_out: bool = False,
        label_revolve_angle_in_degrees: float = 0.0,
        label_rotate_angle_in_degrees: float = 0.0,
        directedness: str = "-",
    ) -> None:
        if isinstance(vertex_one, str):
            vertex_one = self.get_vertex(vertex_one)

        if isinstance(vertex_two, str):
            vertex_two = self.get_vertex(vertex_two)

        edge = Line(vertex_one, vertex_two, color=BLACK, stroke_width=0.75)

        if directedness.endswith(">"):
            edge.add_tip(tip_length=0.1, tip_width=0.075)

        if directedness.startswith("<"):
            edge.add_tip(tip_length=0.1, tip_width=0.075, at_start=True)

        self.add(edge)

    def get_vertex(self, label: str, /) -> Vertex:
        for vertex in self.vertices:
            if vertex.label_is(label):
                return vertex

        raise LookupError(f"Unable to find vertex with label ``{label}``")
