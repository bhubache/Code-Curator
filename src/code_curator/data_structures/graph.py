from __future__ import annotations

import math
import warnings
from typing import Any
from typing import TYPE_CHECKING

import numpy as np
from manim import BLACK
from manim import Circle
from manim import DOWN
from manim import IN
from manim import Line
from manim import Mobject
from manim import ORIGIN
from manim import Point

from code_curator.custom_vmobject import CustomVMobject
from code_curator.data_structures.element import Element

if TYPE_CHECKING:
    from collections.abc import Iterable
    from collections.abc import Sequence
    from colour import Color
    from manim.typing import Vector


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
        label: Any = None,
        *,
        contents: Any = None,
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
        if label is None and contents is None:
            raise ValueError(f"You must provide at least the label or the contents of the {type(self)}")

        if container is None:
            container = Circle(
                color=color,
                radius=radius,
                stroke_width=container_stroke_width,
            )

        if not show_container:
            container.set_opacity(0)

        if position_relative_to is None:
            position_relative_to = ORIGIN
        elif isinstance(position_relative_to, Mobject):
            position_relative_to = position_relative_to.get_center()

        container.move_to(position + np.array(position_relative_to))

        self.add(container)

        if not isinstance(contents, Mobject) and contents is not None:
            contents = Element(
                contents,
                color=color,
                font_size=contents_font_size,
            )

        if contents is not None:
            contents.move_to(container.get_center())
            container.add(contents)

        if show_label and label is None:
            raise ValueError("You must provide a label for it to be shown")

        if not isinstance(label, Mobject) and label is not None:
            label = Element(
                label,
                color=color,
                font_size=DEFAULT_LABEL_FONT_SIZE,
            )

        if show_label:
            self.quasi_add(label)
            label.move_to(container.get_center())

            try:
                container_radius = container.radius
            except AttributeError:
                container_radius = Circle().surround(container, stretch=True, buffer_factor=1).radius

            if label_out:
                buffer_factor = (container_radius + label_dist) / container_radius
            else:
                buffer_factor = label_dist / container_radius

            label_placement_helper_circle = (
                Circle(
                    stroke_width=container.stroke_width,
                )
                .match_style(container)
                .surround(
                    container,
                    stretch=True,
                    buffer_factor=buffer_factor,
                )
            )

            label_placement_helper_circle.move_to(container.get_center())

            label.move_to(
                label_placement_helper_circle.point_at_angle(
                    math.radians(label_revolve_angle_in_degrees),
                ),
            )

            label.rotate(
                math.radians(label_rotate_angle_in_degrees),
                axis=IN,
                about_point=label.get_center(),
            )

        self.label_mobject = label
        self.container = container
        self.contents_mobject = contents

        # TODO: Move to classes that compose emtpy
        if self.contents == "null":
            mock_contents = Element("n")
            mock_contents.move_to(self.container.get_center())
            mock_contents.match_style(self.contents_mobject)
            self.contents_mobject.align_to(mock_contents, DOWN)

    def __str__(self) -> str:
        return str(self.contents)

    @property
    def contents(self):
        if self.contents_mobject is None:
            return None

        return self.contents_mobject.value

    @property
    def label(self):
        if self.label_mobject is None:
            return None

        return self.label_mobject.value

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
        angle_in_degrees: float = 0.0,
    ) -> None:
        super().__init__()
        if not isinstance(vertex_one, Mobject) or not isinstance(vertex_two, Mobject):
            raise TypeError("You must provide Mobjects as the vertices")

        self.vertex_one = vertex_one
        self.vertex_two = vertex_two
        self.line = Line(
            self.vertex_one,
            self.vertex_two,
            color=color,
            stroke_width=line_stroke_width,
            path_arc=math.radians(angle_in_degrees),
        )
        self.directedness = directedness

        # FIXME: It looks like double headed arrow heads aren't the same size
        if directedness.endswith(">"):
            self.line.add_tip(tip_length=tip_length, tip_width=tip_width)

        if directedness.startswith("<"):
            self.line.add_tip(tip_length=tip_length, tip_width=tip_width, at_start=True)

        self.add_updater(self.shortest_path_updater)

        self.add(self.line)

        self.update()

    def __str__(self) -> str:
        if self.directedness.endswith(">"):
            start = self.vertex_one
            end = self.vertex_two
        else:
            start = self.vertex_two
            end = self.vertex_one

        return f"{start} {self.directedness} {end}"

    # TODO: This duplicates code in the __init__
    def shortest_path_updater(self, some_obj) -> None:
        reference_line = Line(
            self.vertex_one.container.get_center(),
            self.vertex_two.container.get_center(),
            color=self.color,
        )

        if hasattr(self, "invisible_to_avoid_divide_by_zero"):
            self.line.restore()
            delattr(self, "invisible_to_avoid_divide_by_zero")

        with warnings.catch_warnings():
            warnings.filterwarnings("error")

            try:
                new_line = Line(
                    reference_line.point_from_proportion(
                        min(1, self.vertex_one.container.radius / reference_line.get_length()),
                    ),
                    reference_line.point_from_proportion(
                        max(0, 1 - (self.vertex_two.container.radius / reference_line.get_length())),
                    ),
                    path_arc=self.line.path_arc,
                )
            except RuntimeWarning:
                self.line.save_state()
                self.set_opacity(0)
                self.invisible_to_avoid_divide_by_zero = True
            else:
                if self.line.has_tip():
                    new_line.add_tip(self.line.tip)
                    new_line.tip.match_style(self.line.tip)

                if self.line.has_start_tip():
                    new_line.add_tip(self.line.start_tip, at_start=True)
                    new_line.start_tip.match_style(self.line.start_tip)

                new_line.match_style(self.line)

                self.line.become(
                    new_line,
                )

    def get_start(self):
        return self.line.get_start()

    def get_end(self):
        return self.line.get_end()

    def get_start_and_end(self):  # noqa: FNE007
        return self.line.get_start_and_end()

    def put_start_and_end_on(
        self,
        start: Iterable[float] | Mobject,
        end: Iterable[float] | Mobject,
    ) -> None:  # noqa: FNE007
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

    def reconnect(self, old_vertex, new_vertex, angle_in_degrees: float) -> None:
        if self.vertex_one == old_vertex:
            self.vertex_one = new_vertex
        else:
            self.vertex_two = new_vertex

        self.line.set_path_arc(math.radians(angle_in_degrees))


class Graph(CustomVMobject):
    def __init__(self) -> None:
        super().__init__()
        self.vertices: set[Vertex] = set()
        self.edges: set[Edge] = set()
        self.labeled_pointers: dict[str, LabeledLine] = {}

    def add_vertex(
        self,
        label_or_vertex: Any,
        quasi: bool = False,
        **kwargs,
    ) -> Vertex:
        if not isinstance(label_or_vertex, Vertex):
            label_or_vertex = Vertex(label_or_vertex, **kwargs)

        if label_or_vertex in self.vertices:
            return label_or_vertex

        if quasi:
            self.quasi_add(label_or_vertex)
        else:
            self.add(label_or_vertex)

        self.vertices.add(label_or_vertex)

        return label_or_vertex

    def add_edge(
        self,
        vertex_one: Any,
        vertex_two: Any,
        quasi: bool = False,
        **kwargs,
    ) -> Edge:
        if not isinstance(vertex_one, Mobject):
            vertex_one = self.get_vertex(vertex_one)

        if not isinstance(vertex_two, Mobject):
            vertex_two = self.get_vertex(vertex_two)

        edge = Edge(
            vertex_one,
            vertex_two,
            **kwargs,
        )

        if quasi:
            self.quasi_add(edge)
        else:
            self.add(edge)

        if edge.vertex_one not in self.vertices:
            self.add_vertex(edge.vertex_one, quasi=quasi)

        if edge.vertex_two not in self.vertices:
            self.add_vertex(edge.vertex_two, quasi=quasi)

        self.edges.add(edge)

        return edge

    def add_labeled_pointer(
        self,
        mobject: Mobject,
        label: str | Element,
        direction: Vector,
        color,
    ) -> None:
        if isinstance(label, Element):
            label = label.value

        self.labeled_pointers[label] = LabeledLine(
            mobject,
            label=label,
            direction=direction,
            color=color,
        )
        self.add(self.labeled_pointers[label])

    def remove_labeled_pointer(self, label: str | Element) -> None:
        if isinstance(label, Element):
            label = label.value

        self.remove(self.labeled_pointers[label])

    def remove(self, *mobjects: Mobject):
        for mob in mobjects:
            if isinstance(mob, Vertex):
                self.vertices.remove(mob)

                for edge in self.edges:
                    if mob is edge.vertex_one:
                        edge.vertex_one = None

                    if mob is edge.vertex_two:
                        edge.vertex_two = None

            elif isinstance(mob, Edge):
                self.edges.remove(mob)
                mob.vertex_one = None
                mob.vertex_two = None
            elif isinstance(mob, LabeledLine):
                del self.labeled_pointers[mob.label]
                self.submobjects.remove(mob)
            else:
                raise NotImplementedError(f"Removing mob {mob} from {self.__class__.__name__} is not yet supported")

            self.submobjects.remove(mob)

    def get_vertex(self, label: str | int, /) -> Vertex:
        for vertex in self.vertices:
            if vertex.label == label:
                return vertex

        raise LookupError(f"Unable to find vertex with label ``{label}``")

    def get_edges_connecting_vertices(self, vertex_one: Vertex, vertex_two: Vertex) -> Sequence[Edge]:
        edges = []
        for edge in self.edges:
            if (edge.vertex_one == vertex_one and edge.vertex_two == vertex_two) or (
                edge.vertex_one == vertex_two and edge.vertex_two == vertex_one
            ):
                edges.append(edge)

        return edges

    def get_edge_from_to(self, from_: Vertex, to: Vertex) -> Edge:
        edges_to_from = []
        for edge in self.get_edges_connecting_vertices(from_, to):
            if edge.vertex_one == from_ and edge.vertex_two == to and edge.directedness == "->":
                edges_to_from.append(edge)
            elif edge.vertex_one == to and edge.vertex_two == from_ and edge.directedness == "<-":
                edges_to_from.append(edge)

        if len(edges_to_from) > 1:
            raise RuntimeError(
                f"There should only be one edge connecting {from_} to {to} but there are {len(edges_to_from)}:"
                f" {edges_to_from}",
            )

        return edges_to_from[0]

    def get_vertices_with_no_incoming_edges(self):
        vertices_with_no_incoming_edges = []
        for vertex in self.vertices:
            for edge in self.edges:
                if vertex is edge.vertex_one and edge.directedness.startswith("<"):
                    break

                if vertex is edge.vertex_two and edge.directedness.endswith(">"):
                    break
            else:
                vertices_with_no_incoming_edges.append(vertex)

        return vertices_with_no_incoming_edges

    def get_vertices_with_no_outgoing_edges(self):
        vertices_with_no_outgoing_edges = []
        for vertex in self.vertices:
            for edge in self.edges:
                if vertex is edge.vertex_one and edge.directedness.endswith(">"):
                    break

                if vertex is edge.vertex_two and edge.directedness.startswith("<"):
                    break
            else:
                vertices_with_no_outgoing_edges.append(vertex)

        return vertices_with_no_outgoing_edges


class LabeledLine(CustomVMobject):
    def __init__(
        self,
        start: tuple[float, float, float] | Mobject,
        end: tuple[float, float, float] | Mobject | None = None,
        *,
        direction: tuple[float, float, float] | None = None,
        label_font_size: float = DEFAULT_LABEL_FONT_SIZE,
        length: float = DEFAULT_LINE_LENGTH,
        label: Any = "",
        label_dist: float = 0.1,
        color: str | Color = DEFAULT_COLOR,
        label_color: str | Color = DEFAULT_COLOR,
        tip_length: float = DEFAULT_TIP_LENGTH,
        tip_width: float = DEFAULT_TIP_WIDTH,
        directedness: str = "->",
    ) -> None:
        super().__init__()
        if end is None:
            if isinstance(start, Mobject):
                end = start.get_boundary_point(-direction)
                self._pointee = start
            else:
                end = start
                self._pointee = Point(end)
                self._pointee.proportion_from_point = lambda _: 0

            start = Point(end).shift(-direction * length)
        elif isinstance(end, Mobject):
            self.pointee = end

        line = Line(
            start,
            end,
            color=color,
            stroke_width=DEFAULT_EDGE_STROKE_WIDTH,
        )

        if directedness.endswith(">"):
            line.add_tip(tip_length=tip_length, tip_width=tip_width)

        if directedness.startswith("<"):
            line.add_tip(tip_length=tip_length, tip_width=tip_width, at_start=True)

        if not isinstance(label, Mobject):
            label = Element(
                label,
                color=color,
                font_size=label_font_size,
            )

        self.add(line)
        self.add(label)

        self.label_mobject = label
        self.line = line
        self.label_dist = label_dist

        label.add_updater(self.label_updater, call_updater=True)

        if isinstance(end, Mobject):
            line.add_updater(self.line_updater, call_updater=True)

        if isinstance(start, Mobject):
            line.add_updater(self.line_updater, call_updater=True)

    @property
    def line_mob_connecting_proportion(self) -> float:
        return self.pointee.proportion_from_point(
            self.pointee.get_boundary_point(-self.line.get_unit_vector()),
        )

    @property
    def start(self) -> Iterable[float]:
        return self.line.get_start()

    @property
    def end(self) -> Iterable[float]:
        return self.line.get_end()

    @property
    def label(self) -> Any:
        return self.label_mobject.value

    @property
    def pointee(self) -> Mobject | Vector:
        return self._pointee

    @pointee.setter
    def pointee(self, new_pointee: Mobject | Vector) -> None:
        self._pointee = new_pointee
        self.update()

    @property
    def direction(self) -> Vector:
        return self.line.get_unit_vector()

    @direction.setter
    def direction(self, new_direction) -> None:
        new_end = self.pointee.get_boundary_point(-new_direction)
        new_start = Point(new_end).shift(-new_direction * self.line.get_length()).get_center()

        self.line.put_start_and_end_on(new_start, new_end)
        # TODO: May have to resume updating?
        self.update()

    def line_updater(self, line):
        current_end = line.get_end()
        new_end = self.pointee.point_from_proportion(
            self.line_mob_connecting_proportion,
        )
        line.shift(new_end - current_end)

    def label_updater(self, label) -> None:
        label.move_to(self.line.get_start())
        label.shift(-self.line.get_unit_vector() * self.label_dist)
