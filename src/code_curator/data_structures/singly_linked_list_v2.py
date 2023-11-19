from __future__ import annotations

from typing import TYPE_CHECKING

from manim import DOWN
from manim import Line
from manim import Mobject
from manim import ORIGIN

from code_curator.custom_vmobject import CustomVMobject
from code_curator.data_structures.graph import Edge
from code_curator.data_structures.graph import Graph
from code_curator.data_structures.graph import LabeledLine
from code_curator.data_structures.graph import Vertex

if TYPE_CHECKING:
    from collections.abc import Hashable
    from collections.abc import Sequence
    from colour import Color

DEFAULT_NODE_RADIUS = 0.5
DEFAULT_FONT_SIZE = 17
DEFAULT_STROKE_WIDTH = 2
DEFAULT_TIP_WIDTH = 0.2
DEFAULT_TIP_LENGTH = 0.2


class SinglyLinkedList(CustomVMobject):
    def __init__(self, *values, show_null: bool = False, color: str | Color = "#FFFFFF") -> None:
        super().__init__()
        self.show_null = show_null
        self.graph = Graph()
        self.color = color

        for index, value in enumerate(values + ("null",) if show_null else ()):
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
                color=self.color,
                radius=DEFAULT_NODE_RADIUS,
                contents_font_size=DEFAULT_FONT_SIZE,
            )
            self.graph.add_vertex(vertex)

        for index in range(len(self.nodes) - 1):
            curr_node = self.get_node(index)
            next_node = self.get_node(index + 1)

            self.graph.add_edge(
                curr_node,
                next_node,
                directedness="->",
                color=self.color,
                line_stroke_width=DEFAULT_STROKE_WIDTH,
                tip_length=DEFAULT_TIP_LENGTH,
                tip_width=DEFAULT_TIP_WIDTH,
            )

        self.labeled_pointers: dict[Hashable, LabeledLine] = {}

        self.labeled_pointers["head"] = LabeledLine(
            self.get_node(0),
            label="head",
            direction=DOWN,
            color=self.color,
        )
        self.labeled_pointers["tail"] = LabeledLine(
            self.get_node(len(self.values) - 1),
            label="tail",
            direction=DOWN,
            color=self.color,
        )

        self.add(self.graph)
        self.add(self.head_pointer)
        self.add(self.tail_pointer)

        self.move_to(ORIGIN)

    def __len__(self) -> int:
        return len(self.graph.vertices)

    def __iter__(self):
        self.iteration_counter: int = 0
        return self

    def __next__(self):
        try:
            node = self.get_node(self.iteration_counter)
        except IndexError as exc:
            raise StopIteration() from exc
        else:
            self.iteration_counter += 1
            return node

    @property
    def values(self):
        return [node.value for node in self.graph.vertices if node.value != "null"]

    @property
    def nodes(self) -> list[Node]:
        return self.graph.vertices

    @property
    def pointers(self) -> list[Edge]:
        return [node.next_pointer for node in self.nodes if node.next_pointer is not None]

    @property
    def head_pointer(self) -> LabeledLine:
        return self.labeled_pointers["head"]

    @property
    def tail_pointer(self) -> LabeledLine:
        return self.labeled_pointers["tail"]

    def copy(self) -> SinglyLinkedList:
        copy = super().copy()

        # Update references in updaters
        copy.clear_updaters()
        for edge in copy.graph.edges:
            edge.add_updater(edge.shortest_path_updater)

        return copy

    def create_reset_copy(self, remove_indices: Sequence[int] = ()) -> SinglyLinkedList:
        fresh_linked_list = SinglyLinkedList(
            *[value for index, value in enumerate(self.values) if index not in remove_indices],
            show_null=self.show_null,
            color=self.color,
        )

        copy = self.copy()
        for index in remove_indices:
            node_to_remove = copy.get_node(index)
            if node_to_remove is not None and node_to_remove.next_pointer is not None:
                copy.remove(node_to_remove.next_pointer)
            elif node_to_remove is not None:
                copy.remove(node_to_remove)

        for old_pointer, new_pointer in zip(copy.pointers, fresh_linked_list.pointers):
            old_pointer.become(new_pointer)

        copy.become(fresh_linked_list)
        for label in fresh_linked_list.labeled_pointers:
            copy.labeled_pointers[label].become(fresh_linked_list.labeled_pointers[label])

        for label in set(copy.labeled_pointers.keys()) - set(fresh_linked_list.labeled_pointers.keys()):
            copy.remove_labeled_pointer(label)

        return copy

    def remove(self, *mobjects: Mobject):
        for mob in mobjects:
            if isinstance(mob, (Vertex, Edge)):
                self.graph.remove(mob)
            elif isinstance(mob, LabeledLine):
                del self.labeled_pointers[mob.label.value]
                self.submobjects.remove(mob)
            else:
                raise NotImplementedError(f"Removal of mobject {mob} from SLL not yet supported")

    def get_node(self, index: int) -> Node:
        return self.nodes[index]

    def add_labeled_pointer(self, index: int, label, direction: tuple[float, float, float] | None = None) -> None:
        if direction is None:
            direction = -self.head_pointer.direction

        self.labeled_pointers[label] = LabeledLine(self.get_node(index), label=label, direction=direction)
        self.add(self.labeled_pointers[label])

    def remove_labeled_pointer(self, label) -> None:
        self.remove(self.labeled_pointers[label])


class Node(Vertex):
    def __init__(self, edges, **kwargs) -> None:
        super().__init__(**kwargs)
        self.edges = edges

    def __repr__(self) -> str:
        return f"Node({self.value})"

    @property
    def next_pointer(self) -> Line:
        try:
            return [edge for edge in self.edges if edge.vertex_one is self][0]
        except IndexError:
            pass  # The last node has no next pointer
