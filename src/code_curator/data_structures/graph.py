from __future__ import annotations

import collections
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
    _default_label: int = 0

    def __init__(
        self,
        label: str | Mobject | None = None,
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
        show_container: bool = True,
    ) -> None:
        super().__init__()
        if label is None:
            label = f"Label{Vertex._default_label}"
            Vertex._default_label += 1

        if not isinstance(label, Mobject):
            label = Element(label, color=BLACK, font_size=DEFAULT_ELEMENT_FONT_SIZE - 2)

        if container is None:
            container = Circle(color=BLACK, radius=0.2, stroke_width=0.75)

        self.label = label
        self.container = container
        self.contents = contents

        if not show_container:
            self.container.set_opacity(0)

        if self.contents is not None:
            self.contents = Element(
                contents,
                color=BLACK,
                font_size=DEFAULT_ELEMENT_FONT_SIZE - 2,
            )
            self.container.add(self.contents)

        self.container.move_to(position)

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

        self.add(container)
        if show_label:
            self.add(label)

    def label_is(self, value: str) -> bool:
        return self.label.value == value


class Graph(CustomVMobject):
    def __init__(self) -> None:
        super().__init__()
        self.vertices: set[Vertex] = set()
        self.adjacency_list: dict[Vertex, list[Vertex]] = collections.defaultdict(list)

    def add_vertex(
        self,
        label_or_vertex: str | Vertex | None = None,
        **kwargs,
    ) -> None:
        if not isinstance(label_or_vertex, Vertex):
            label_or_vertex = Vertex(label_or_vertex, **kwargs)

        self.add(label_or_vertex)
        self.vertices.add(label_or_vertex)
        if label_or_vertex not in self.adjacency_list:
            self.adjacency_list[label_or_vertex] = []

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

        def shortest_path_updater(edge_to_update: Line) -> None:
            reference_line = Line(
                vertex_one.container.get_center(),
                vertex_two.container.get_center(),
                color=BLACK,
            )

            edge_to_update.become(
                Line(
                    reference_line.point_from_proportion(
                        vertex_one.container.radius / reference_line.get_length(),
                    ),
                    reference_line.point_from_proportion(
                        1 - (vertex_two.container.radius / reference_line.get_length()),
                    ),
                )
                .add_tip(edge_to_update.tip)
                .match_style(edge_to_update),
            )

        edge.add_updater(shortest_path_updater)
        edge.add_updater(shortest_path_updater)

        self.add(edge)

        self.adjacency_list[vertex_one].append(vertex_two)

        self.vertices.add(vertex_one)
        self.vertices.add(vertex_two)

    def get_vertex(self, label: str, /) -> Vertex:
        for vertex in self.vertices:
            if vertex.label_is(label):
                return vertex

        raise LookupError(f"Unable to find vertex with label ``{label}``")
