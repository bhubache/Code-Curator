from __future__ import annotations

import itertools as it
from collections.abc import Iterable
from typing import TYPE_CHECKING

from manim import Animation
from manim import CurvedArrow
from manim import DOWN
from manim import Line
from manim import Mobject
from manim import ORIGIN

from code_curator.animations.singly_linked_list.transform_sll import TransformSinglyLinkedList
from code_curator.custom_vmobject import CustomVMobject
from code_curator.data_structures.element import Element
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


# TODO: Add more flexible positioning options
RELATIVE_POSITION = (2.0, 0.0, 0.0)


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
                position=RELATIVE_POSITION,
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
    
    def reset_positioning(self) -> None:
        for prev_node, next_node in it.pairwise(self.nodes):
            relative_center = prev_node.get_center()
            next_node.move_to(relative_center + RELATIVE_POSITION)

        self.move_to(ORIGIN)
        self.resume_updating()
        self.update()

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

    def get_node_index(self, node: Node) -> int:
        return self.nodes.index(node)

    def add_labeled_pointer(
        self, index: int, label: str | Element, direction: tuple[float, float, float] | None = None
    ) -> None:
        if isinstance(label, Element):
            label = label.value

        if direction is None:
            direction = -self.head_pointer.direction

        self.labeled_pointers[label] = LabeledLine(
            self.get_node(index), label=label, direction=direction, color=self.color
        )
        self.add(self.labeled_pointers[label])

    def remove_labeled_pointer(self, label: str | Element) -> None:
        if isinstance(label, Element):
            label = label.value

        self.remove(self.labeled_pointers[label])

    def get_labeled_pointer(self, name: str) -> LabeledLine:
        return self.labeled_pointers[name]

    def move_labeled_pointer(self, pointer: str | LabeledLine, num_nodes: int = 1) -> tuple[SinglyLinkedList, Animation]:
        copy = self._create_animation_copy()
        if isinstance(pointer, str):
            labeled_pointer = copy.get_labeled_pointer(pointer)
        else:
            labeled_pointer = copy.get_labeled_pointer(pointer.label)

        old_node_index: int = copy.nodes.index(labeled_pointer.pointee)
        new_node_index: int = old_node_index + num_nodes
        copy.get_labeled_pointer(labeled_pointer.label.value).shift(
            copy.get_node(new_node_index).get_center() - copy.get_node(old_node_index).get_center(),
        )
        copy.get_labeled_pointer(labeled_pointer.label.value).pointee = copy.get_node(new_node_index)

        return copy, TransformSinglyLinkedList(
            self,
            copy,
        )

    def shrink_pointer(self, pointer: Edge) -> tuple[SinglyLinkedList, Animation]:
        node_index: int = self.get_next_pointers_node_index(pointer)

        copy = self._create_animation_copy()
        start = self.get_node(node_index).next_pointer.get_start()
        copy.get_node(node_index).next_pointer.put_start_and_end_on(start, start)
        return copy, TransformSinglyLinkedList(
            self,
            copy,
        )

    def grow_pointer(self, pointer: Edge) -> tuple[SinglyLinkedList, Animation]:
        node_index: int = self.get_next_pointers_node_index(pointer)

        copy = self._create_animation_copy()
        copy_next_pointer = copy.get_node(node_index).next_pointer
        copy_next_pointer.put_start_and_end_on(
            copy_next_pointer.get_start(),
            copy_next_pointer.vertex_two,
        )
        return copy, TransformSinglyLinkedList(
            self,
            copy,
        )

    def curve_pointer_to(self, pointer: Edge, node: Node) -> tuple[SinglyLinkedList, Animation]:
        node_index_from: int = self.get_node_index(pointer.vertex_one)
        node_index_to: int = self.get_node_index(node)
        copy = self._create_animation_copy()

        node_from_copy = copy.get_node(node_index_from)
        prev_node_to_copy = copy.get_node(node_index_to - 1)

        node_from_copy.next_pointer.become(
            CurvedArrow(
                pointer.get_start(),
                prev_node_to_copy.next_pointer.get_end(),
                tip_length=prev_node_to_copy.next_pointer.get_tip().length,
            )
        )

        node_from_copy.next_pointer.vertex_two = copy.get_node(node_index_to)
        return copy, TransformSinglyLinkedList(
            self,
            copy,
        )

    def fade_out_components(self, *components: Mobject) -> tuple[SinglyLinkedList, Animation]:
        copy = self._create_animation_copy()
        for copied_component in self._get_copy_components(*components, copy=copy):
            copy.remove(copied_component)

        return copy, TransformSinglyLinkedList(
            self,
            copy,
        )
    
    def flatten(self) -> tuple[SinglyLinkedList, Animation]:
        copy = self._create_animation_copy()
        copy.reset_positioning()

        return copy, TransformSinglyLinkedList(
            self,
            copy,
        )

    def _get_copy_components(self, *original_components: Mobject, copy: SinglyLinkedList) -> Iterable[Mobject]:
        copied_components = []

        for component in original_components:
            if isinstance(component, LabeledLine):
                copied_components.append(copy.labeled_pointers[component.label])
            elif isinstance(component, Node):
                copied_components.append(
                    copy.get_node(self.get_node_index(component)),
                )
            elif isinstance(component, Edge):
                copied_components.append(
                    copy.get_node(self.get_node_index(component.vertex_one)).next_pointer,
                )
            else:
                raise NotImplementedError(f"Unexpected component type: {type(component)}")

        return copied_components

    def get_next_pointers_node_index(self, pointer: Edge) -> int:
        return [index for index, node in enumerate(self.nodes) if node.next_pointer is pointer][0]

    def _create_animation_copy(self) -> SinglyLinkedList:
        attr_name = "_copy_for_animation"
        if not hasattr(self, attr_name):
            setattr(self, attr_name, self.copy())

        return getattr(self, attr_name)


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
