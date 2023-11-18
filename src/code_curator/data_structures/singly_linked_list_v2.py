from __future__ import annotations

from typing import TYPE_CHECKING

from manim import DOWN
from manim import ORIGIN

from code_curator.custom_vmobject import CustomVMobject
from code_curator.data_structures.graph import Graph
from code_curator.data_structures.graph import LabeledLine
from code_curator.data_structures.graph import Vertex

if TYPE_CHECKING:
    from collections.abc import Hashable
    from colour import Color

DEFAULT_NODE_RADIUS = 0.5
DEFAULT_FONT_SIZE = 17
DEFAULT_STROKE_WIDTH = 2
DEFAULT_TIP_WIDTH = 0.2
DEFAULT_TIP_LENGTH = 0.2


class SinglyLinkedList(CustomVMobject):
    def __init__(self, *values, show_null: bool = False, color: str | Color = "#FFFFFF") -> None:
        super().__init__()
        self.values = values
        self.show_null = show_null
        self.graph = Graph()

        for index, value in enumerate(self.values + ("null",) if show_null else ()):
            if index == 0:
                position_relative_to = ORIGIN
            else:
                position_relative_to = self.get_node(index - 1)

            vertex = Node(
                edges=self.graph.edges,
                label=index,
                contents=value,
                show_label=False,
                position=(2.0, 0.0, 0.0),
                position_relative_to=position_relative_to,
                show_container=value != "null",
                container_stroke_width=DEFAULT_STROKE_WIDTH,
                color=color,
                radius=DEFAULT_NODE_RADIUS,
                contents_font_size=DEFAULT_FONT_SIZE,
            )
            self.graph.add_vertex(vertex)

        for index in range(len(self.values) - 0 if show_null else 1):
            curr_node = self.get_node(index)
            next_node = self.get_node(index + 1)

            self.graph.add_edge(
                curr_node,
                next_node,
                directedness="->",
                color=color,
                line_stroke_width=DEFAULT_STROKE_WIDTH,
                tip_length=DEFAULT_TIP_LENGTH,
                tip_width=DEFAULT_TIP_WIDTH,
            )

        self.labeled_pointers: dict[Hashable, LabeledLine] = {}

        self.labeled_pointers["head"] = LabeledLine(
            self.get_node(0),
            label="head",
            direction=DOWN,
            color=color,
            label_font_size=DEFAULT_FONT_SIZE,
        )
        self.labeled_pointers["tail"] = LabeledLine(
            self.get_node(len(self.values) - 1),
            label="tail",
            direction=DOWN,
            color=color,
        )

        self.add(self.graph)
        self.add(self.head_pointer)
        self.add(self.tail_pointer)

        self.move_to(ORIGIN)

    def __len__(self) -> int:
        return len(self.values)

    def __iter__(self):
        self.iteration_counter: int = 0
        return self

    def __next__(self):
        try:
            node = self.get_node(self.iteration_counter)
        except IndexError:
            raise StopIteration()
        else:
            self.iteration_counter += 1
            return node

    @property
    def head_pointer(self) -> LabeledLine:
        return self.labeled_pointers["head"]

    @property
    def tail_pointer(self) -> LabeledLine:
        return self.labeled_pointers["tail"]

    def get_node(self, index: int) -> Node:
        try:
            return self.graph.get_vertex(index)
        except LookupError:
            raise IndexError(f"Index {index} out of bounds for length {len(self)}")

    def add_labeled_pointer(self, index: int, label, direction: tuple[float, float, float] | None = None) -> None:
        if direction is None:
            direction = -self.head_pointer.direction

        self.labeled_pointers[label] = LabeledLine(self.get_node(index), label=label, direction=direction)
        self.add(self.labeled_pointers[label])

    def remove_labeled_pointer(self, label) -> None:
        self.remove(self.labeled_pointers[label])
        del self.labeled_pointers[label]


class Node(Vertex):
    def __init__(self, edges, **kwargs) -> None:
        super().__init__(**kwargs)
        self.edges = edges

    @property
    def next_pointer(self):
        try:
            return [edge for edge in self.edges if edge.vertex_one is self][0]
        except IndexError:
            pass  # The last node has no next pointer
