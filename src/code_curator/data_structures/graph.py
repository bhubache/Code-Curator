from __future__ import annotations

import collections
import math
from typing import TYPE_CHECKING

import numpy as np
from manim import BLACK
from manim import Circle
from manim import Dot
from manim import DOWN
from manim import Line
from manim import Mobject

from code_curator.custom_vmobject import CustomVMobject
from code_curator.data_structures.element import Element

if TYPE_CHECKING:
    from colour import Color


DEFAULT_COLOR = BLACK
DEFAULT_LABEL_FONT_SIZE = 15
DEFAULT_CONTENTS_FONT_SIZE = 15
DEFAULT_VERTEX_RADIUS = 0.2
DEFAULT_VERTEX_STROKE_WIDTH = 0.75
DEFAULT_TIP_LENGTH = 0.1
DEFAULT_TIP_WIDTH = 0.075
DEFAULT_EDGE_STROKE_WIDTH = 0.75
DEFAULT_LINE_LENGTH = 0.75


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
            label = Element(
                label,
                color=DEFAULT_COLOR,
                font_size=DEFAULT_LABEL_FONT_SIZE,
            )

        if container is None:
            container = Circle(
                color=DEFAULT_COLOR,
                radius=DEFAULT_VERTEX_RADIUS,
                stroke_width=DEFAULT_VERTEX_STROKE_WIDTH,
            )

        self.label = label
        self.container = container
        self.contents = contents

        if not show_container:
            self.container.set_opacity(0)

        if self.contents is not None:
            self.contents = Element(
                contents,
                color=DEFAULT_COLOR,
                font_size=DEFAULT_CONTENTS_FONT_SIZE,
            )
            self.container.add(self.contents)

        self.container.move_to(position)

        if label_out:
            circumscribing_circle = Circle(
                stroke_width=container.stroke_width,
            ).surround(
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

        if self.contents is not None and self.contents.value == "null":
            mock_contents = Element("n")
            mock_contents.move_to(self.container.get_center())
            mock_contents.match_style(self.contents)
            self.contents.align_to(mock_contents, DOWN)

    def label_is(self, value: str) -> bool:
        return self.label.value == value

    def proportion_from_point(self, point) -> float:
        return self.container.proportion_from_point(point)

    def point_from_proportion(self, alpha: float) -> np.ndarray:
        return self.container.point_from_proportion(alpha)


class Edge(CustomVMobject):
    def __init__(
        self,
        vertex_one: Vertex,
        vertex_two: Vertex,
        *,
        label: str | None = None,
        color: str | Color = BLACK,
        opacity: float = 1.0,
        line_stroke_width: float = DEFAULT_EDGE_STROKE_WIDTH,
        label_distance_proportion: float = 0.5,
        label_line_sep: float = 0.1,
        label_container: Mobject | None = None,
        label_out: bool = False,
        label_revolve_angle_in_degrees: float = 0.0,
        label_rotate_angle_in_degrees: float = 0.0,
        tip_length: float = DEFAULT_TIP_LENGTH,
        tip_width: float = DEFAULT_TIP_WIDTH,
        directedness: str = "-",
    ) -> None:
        super().__init__()
        self.vertex_one = vertex_one
        self.vertex_two = vertex_two
        self.line = Line(
            self.vertex_one,
            self.vertex_two,
            color=DEFAULT_COLOR,
            stroke_width=line_stroke_width,
        )

        if directedness.endswith(">"):
            self.line.add_tip(tip_length=tip_length, tip_width=tip_width)

        if directedness.startswith("<"):
            self.line.add_tip(tip_length=tip_length, tip_width=tip_width, at_start=True)

        def shortest_path_updater(edge_to_update: Line) -> None:
            reference_line = Line(
                self.vertex_one.container.get_center(),
                self.vertex_two.container.get_center(),
                color=BLACK,
            )
            edge_to_update.become(
                Line(
                    reference_line.point_from_proportion(
                        min(1, self.vertex_one.container.radius / reference_line.get_length()),
                    ),
                    reference_line.point_from_proportion(
                        max(0, 1 - (self.vertex_two.container.radius / reference_line.get_length())),
                    ),
                )
                .add_tip(edge_to_update.tip)
                .match_style(edge_to_update),
            )

        self.line.add_updater(shortest_path_updater, call_updater=True)
        self.line.add_updater(shortest_path_updater, call_updater=True)

        self.add(self.line)


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
        **kwargs,
    ) -> None:
        if isinstance(vertex_one, str):
            vertex_one = self.get_vertex(vertex_one)

        if isinstance(vertex_two, str):
            vertex_two = self.get_vertex(vertex_two)

        edge = Edge(
            vertex_one,
            vertex_two,
            **kwargs,
        )
        self.add(edge)

        self.adjacency_list[edge.vertex_one].append(edge.vertex_two)

        self.vertices.add(edge.vertex_one)
        self.vertices.add(edge.vertex_two)

    def get_vertex(self, label: str, /) -> Vertex:
        for vertex in self.vertices:
            if vertex.label_is(label):
                return vertex

        raise LookupError(f"Unable to find vertex with label ``{label}``")


class LabeledLine(CustomVMobject):
    def __init__(
        self,
        start: tuple[float, float, float] | Mobject,
        end: tuple[float, float, float] | Mobject | None = None,
        *,
        direction: tuple[float, float, float] | None = None,
        length: float = DEFAULT_LINE_LENGTH,
        label: str | Mobject = "",
        label_dist: float = 0.1,
        color: str | Color = DEFAULT_COLOR,
        label_color: str | Color = DEFAULT_COLOR,
        tip_length: float = DEFAULT_TIP_LENGTH,
        tip_width: float = DEFAULT_TIP_WIDTH,
        directedness: str = "->",
    ) -> None:
        super().__init__()
        if isinstance(label, str):
            label = Element(
                label,
                color=DEFAULT_COLOR,
                font_size=DEFAULT_LABEL_FONT_SIZE,
            )

        if end is None:
            # Assume user passed in the location/Mobject they want the line to point to
            end = start.get_boundary_point(-direction)
            target_mobject = start
            start = Dot(end).shift(-direction * length)
        else:
            raise NotImplementedError()

        self.line = Line(
            start,
            end,
            color=DEFAULT_COLOR,
            stroke_width=DEFAULT_EDGE_STROKE_WIDTH,
        )
        self.label = label

        if target_mobject:
            self.line_mob_connecting_proportion: float = target_mobject.proportion_from_point(
                target_mobject.get_boundary_point(-self.line.get_unit_vector()),
            )

        self.label_dist = label_dist
        if directedness.endswith(">"):
            self.line.add_tip(tip_length=tip_length, tip_width=tip_width)

        if directedness.startswith("<"):
            self.line.add_tip(tip_length=tip_length, tip_width=tip_width, at_start=True)

        def line_updater(line) -> None:
            current_end = line.get_end()
            new_end = target_mobject.point_from_proportion(
                self.line_mob_connecting_proportion,
            )
            line.shift(new_end - current_end)

        if isinstance(end, Mobject):
            self.line.add_updater(line_updater)

        if isinstance(start, Mobject):
            self.line.add_updater(line_updater)

        def label_updater(label) -> None:
            label.move_to(self.line.get_start())
            label.shift(-self.line.get_unit_vector() * self.label_dist)

        self.label.add_updater(label_updater, call_updater=True)

        self.add(self.line)
        self.add(self.label)
