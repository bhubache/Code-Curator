from __future__ import annotations

import collections
import math
from collections.abc import Iterable
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
    def __init__(
        self,
        label: str | Mobject | None = None,
        *,
        contents: str | Mobject | None = None,
        contents_font_size: float = DEFAULT_LABEL_FONT_SIZE,
        position_relative_to: tuple[float, float, float] | Mobject | None = None,
        color: str | Color = DEFAULT_COLOR,
        container: Mobject | None = None,
        container_stroke_width: float = DEFAULT_VERTEX_STROKE_WIDTH,
        radius: float = DEFAULT_VERTEX_RADIUS,
        position: tuple[float, float, float] = (0.0, 0.0, 0.0),
        label_out: bool = False,
        label_dist: float = 0.0,
        label_revolve_angle_in_degrees: float = 0.0,
        label_rotate_angle_in_degrees: float = 0.0,
        show_label: bool = True,
        show_container: bool = True,
    ) -> None:
        super().__init__()
        if not isinstance(label, Mobject):
            label = Element(
                label,
                color=color,
                font_size=DEFAULT_LABEL_FONT_SIZE,
            )

        if container is None:
            container = Circle(
                color=color,
                radius=radius,
                stroke_width=container_stroke_width,
            )

        self.label = label
        self.container = container
        self.contents = contents

        if not show_container:
            self.container.set_opacity(0)

        if self.contents is not None:
            self.contents = Element(
                contents,
                color=color,
                font_size=contents_font_size,
            )
            self.container.add(self.contents)

        if position_relative_to is None:
            position_relative_to = np.array([0.0, 0.0, 0.0])
        elif isinstance(position_relative_to, Mobject):
            position_relative_to = position_relative_to.get_center()

        self.container.move_to(position + position_relative_to)

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

    @property
    def value(self):
        return self.contents.value

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
            color=color,
            stroke_width=line_stroke_width,
        )

        if directedness.endswith(">"):
            self.line.add_tip(tip_length=tip_length, tip_width=tip_width)

        if directedness.startswith("<"):
            self.line.add_tip(tip_length=tip_length, tip_width=tip_width, at_start=True)

        self.add_updater(self.shortest_path_updater)

        self.add(self.line)

    def __deepcopy__(self, memodict):
        copy = super().__deepcopy__(memodict)
        copy.add_updater(copy.shortest_path_updater)
        return copy

    def shortest_path_updater(self, some_obj) -> None:
        reference_line = Line(
            self.vertex_one.container.get_center(),
            self.vertex_two.container.get_center(),
            color=self.color,
        )
        self.line.become(
            Line(
                reference_line.point_from_proportion(
                    min(1, self.vertex_one.container.radius / reference_line.get_length()),
                ),
                reference_line.point_from_proportion(
                    max(0, 1 - (self.vertex_two.container.radius / reference_line.get_length())),
                ),
            )
            .add_tip(self.line.tip)
            .match_style(self.line),
        )

    def get_start(self):
        return self.line.get_start()

    def get_end(self):
        return self.line.get_end()

    def get_start_and_end(self):  # noqa: FNE007
        return self.line.get_start_and_end()

    def put_start_and_end_on(self, start: Iterable[float] | Mobject, end: Iterable[float] | Mobject) -> None:  # noqa: FNE007
        arrow_tip_padding = 0
        if isinstance(start, Mobject) or isinstance(end, Mobject):
            new_line = Line(start, end)
        else:
            if np.array_equal(start, end):
                arrow_tip_padding = self.line.tip.length

            new_line = Line(start, [end[0] + arrow_tip_padding, end[1], end[2]])

        new_line.add_tip(self.line.get_tip())
        new_line.match_style(self.line)
        self.line.become(new_line)

    def get_tip(self):
        return self.line.get_tip()

    def become(self, *args, **kwargs):
        old_line_copy = self.line.copy()
        self.line.become(*args, **kwargs).match_style(old_line_copy).get_tip().match_style(old_line_copy.get_tip())

        return self


class Graph(CustomVMobject):
    def __init__(self) -> None:
        super().__init__()
        self.vertices: list[Vertex] = []
        self.edges: set[Edge] = set()
        self.adjacency_list: dict[Vertex, list[Vertex]] = collections.defaultdict(list)

        self.default_vertex_label_counter: int = 0

    def add_vertex(
        self,
        label_or_vertex: str | Vertex | None = None,
        **kwargs,
    ) -> None:
        if not isinstance(label_or_vertex, Vertex):
            label_or_vertex = Vertex(label_or_vertex, **kwargs)

        if label_or_vertex in self.vertices:
            return

        self.add(label_or_vertex)
        self.vertices.append(label_or_vertex)
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

        if edge.vertex_one not in self.vertices:
            self.vertices.append(edge.vertex_one)

        if edge.vertex_two not in self.vertices:
            self.vertices.append(edge.vertex_two)

        self.edges.add(edge)

    def remove(self, *mobjects: Mobject):
        for mob in mobjects:
            if isinstance(mob, Vertex):
                self.vertices.remove(mob)
                del self.adjacency_list[mob]
                for vertex in self.adjacency_list:
                    try:
                        self.adjacency_list[vertex].remove(mob)
                    except ValueError:
                        pass

                for edge in self.edges:
                    if mob is edge.vertex_one:
                        edge.vertex_one = None

                    if mob is edge.vertex_two:
                        edge.vertex_two = None

            elif isinstance(mob, Edge):
                self.edges.remove(mob)
                mob.vertex_one = None
                mob.vertex_two = None
            else:
                raise NotImplementedError(f"Removing mob {mob} from {self.__class__.__name__} is not yet supported")

            self.submobjects.remove(mob)

    def get_vertex(self, label: str | int, /) -> Vertex:
        if isinstance(label, int):
            return self.vertices[label]

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
        label_font_size: float = DEFAULT_LABEL_FONT_SIZE,
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
                color=color,
                font_size=label_font_size,
            )

        if end is None:
            # Assume user passed in the location/Mobject they want the line to point to
            end = start.get_boundary_point(-direction)
            target_mobject = start
            self.pointee = start
            start = Dot(end).shift(-direction * length)
        else:
            raise NotImplementedError()

        self.line = Line(
            start,
            end,
            color=color,
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
            self.line.add_updater(self.line_updater)

        if isinstance(start, Mobject):
            self.line.add_updater(self.line_updater)

        def label_updater(label) -> None:
            label.move_to(self.line.get_start())
            label.shift(-self.line.get_unit_vector() * self.label_dist)

        # self.label.add_updater(label_updater, call_updater=True)
        self.label.add_updater(self.label_updater, call_updater=True)

        self.add(self.line)
        self.add(self.label)

    def line_updater(self, line):
        current_end = line.get_end()
        new_end = self.pointee.point_from_proportion(
            self.line_mob_connecting_proportion,
        )
        line.shift(new_end - current_end)

    def label_updater(self, label) -> None:
        label.move_to(self.line.get_start())
        label.shift(-self.line.get_unit_vector() * self.label_dist)

    # TODO: Fix updaters when copying
    # def __deepcopy__(self, memodict):
    #     copy = super().__deepcopy__(memodict)
    #     # TODO: Add updater for start if start is tied to a mobject and not just a coordinate

    #     copy.line.add_updater(self.line_updater)
    #     return copy


    @property
    def direction(self) -> tuple[float, float, float]:
        return self.line.get_unit_vector()
