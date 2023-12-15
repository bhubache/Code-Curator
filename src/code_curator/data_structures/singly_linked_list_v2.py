from __future__ import annotations

import itertools as it
from typing import TYPE_CHECKING

import numpy as np
from manim import Animation
from manim import CurvedArrow
from manim import DOWN
from manim import Mobject
from manim import ORIGIN
from manim import UP
from manim import WHITE

from code_curator.animations.singly_linked_list.transform_sll import TransformSinglyLinkedList
from code_curator.custom_vmobject import CustomVMobject
from code_curator.data_structures.element import Element
from code_curator.data_structures.graph import Edge
from code_curator.data_structures.graph import Graph
from code_curator.data_structures.graph import LabeledLine
from code_curator.data_structures.graph import Vertex

if TYPE_CHECKING:
    from collections.abc import Hashable
    from collections.abc import Iterable
    from colour import Color

DEFAULT_NODE_RADIUS = 0.5
DEFAULT_FONT_SIZE = 17
DEFAULT_STROKE_WIDTH = 2
DEFAULT_TIP_WIDTH = 0.2
DEFAULT_TIP_LENGTH = 0.2

# TODO: Add more flexible positioning options
RELATIVE_POSITION = (2.0, 0.0, 0.0)

# TODO: Undo operation!!!
# TODO: Make methods like insert_node work with ``animate`` attribute


class SinglyLinkedList(CustomVMobject):
    _node_counter: int = 0

    def __init__(
        self,
        *values,
        color: str | Color = WHITE,
    ) -> None:
        super().__init__()
        self.graph = Graph()
        self.color = color
        self.labeled_pointers: dict[Hashable, LabeledLine] = {}

        self.add(self.graph)

        for index, value in enumerate(values):
            self.insert_node(index, value)

        self.move_to(ORIGIN)

    def __str__(self):
        string = ""
        for node in self.nodes:
            string += f"{node} -> "

        if self.has_null:
            string += "null"
        else:
            string = string[:-4]

        return string

    def __len__(self) -> int:
        return len(self.nodes)

    def __iter__(self):
        return self

    def __next__(self):
        yield from self.nodes

        if self.show_null:
            yield self.null

    def __getitem__(self, item: int) -> Node:
        return self.nodes[item]

    @property
    def head(self) -> Node | None:
        heads = self.graph.get_vertices_with_no_incoming_edges()

        if len(heads) > 3:
            raise RuntimeError(f"BUG: SLL has more than one head: {heads}")

        if len(heads) == 2:
            newest_node = None
            actual_head = None
            for head_candidate in heads:
                trav = head_candidate
                while self.has_next(trav):
                    trav = self.get_next(trav)

                if newest_node is None:
                    newest_node = trav
                    actual_head = head_candidate
                else:
                    if trav.label > newest_node.label:
                        newest_node = trav
                        actual_head = head_candidate

            return actual_head

        try:
            return heads[0]
        except IndexError:
            return None

    @property
    def tail(self) -> Node | None:
        try:
            return self.get_node(-1)
        except IndexError:
            if self.has_null:
                return self.null

            return None

    @property
    def values(self):
        return [node.value for node in self.nodes]

    @property
    def nodes(self) -> list[Node]:
        if self.head is self.null:
            return []

        nodes = []
        trav = self.head
        while trav is not self.null:
            nodes.append(trav)
            trav = self.get_next(trav)

        return nodes

    @property
    def head_pointer(self) -> LabeledLine | None:
        try:
            return self.labeled_pointers["head"]
        except LookupError:
            return None

    @property
    def tail_pointer(self) -> LabeledLine | None:
        try:
            return self.labeled_pointers["tail"]
        except LookupError:
            return None

    @property
    def null(self):
        try:
            return [vertex for vertex in self.graph.vertices if vertex.contents == "null"][0]
        except IndexError:
            return None

    @property
    def has_null(self) -> bool:
        return self.null is not None

    @property
    def has_head(self) -> bool:
        return self.head is not None

    @property
    def has_tail(self) -> bool:
        return self.tail is not None

    @property
    def has_head_pointer(self) -> bool:
        return self.head_pointer is not None

    @property
    def has_tail_pointer(self) -> bool:
        return self.tail_pointer is not None

    @classmethod
    def create_sll(cls, *values, color: str | Color = "#FFFFFF"):
        return SinglyLinkedList(*values, color=color)

    def add_null(self, center: bool = True):
        if self.has_null:
            return self

        if self.has_tail:
            null = self.create_node("null", position_relative_to=self.tail)
            self.set_next(self.tail, null)
        else:
            position_relative_to = ORIGIN
            null = self.create_node("null", position_relative_to=position_relative_to, position=ORIGIN)
            self.graph.add_vertex(null)

        if center:
            self.move_to(ORIGIN)

        return self

    def remove_null(self):
        raise NotImplementedError()
        return self

    def add_head_pointer(self, center: bool = True):
        if not self.has_head:
            raise RuntimeError("Unable to add head pointer because no head is present")

        self.labeled_pointers["head"] = LabeledLine(
            self.head,
            label="head",
            direction=DOWN,
            color=self.color,
        )
        self.add(self.labeled_pointers["head"])
        self.add_updater(self.head_pointer_updater)

        if center:
            self.move_to(ORIGIN)

        return self

    # TODO: Understand if it'd be better to use arg rather than self
    def head_pointer_updater(self, _) -> None:
        self.head_pointer.pointee = self.head
        self.head_pointer.update()

    def remove_head_pointer(self):
        raise NotImplementedError()

    def add_tail_pointer(self, center: bool = True):
        if not self.has_tail:
            raise RuntimeError("Unable to add tail pointer because no tail is present")

        if self.head == self.tail:
            tail_direction = UP
        else:
            tail_direction = DOWN

        self.labeled_pointers["tail"] = LabeledLine(
            self.tail,
            label="tail",
            direction=tail_direction,
            color=self.color,
        )
        self.add(self.labeled_pointers["tail"])
        self.add_updater(self.tail_pointer_updater)

        if center:
            self.move_to(ORIGIN)

        return self

    def tail_pointer_updater(self, _) -> None:
        self.tail_pointer.pointee = self.tail
        if np.array_equal(self.tail_pointer.direction, UP) and self.head is not self.tail:
            self.tail_pointer.direction = DOWN

        self.tail_pointer.update()

    def remove_tail_pointer(self):
        raise NotImplementedError()

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

    def get_next(self, curr_node):
        for edge in self.graph.edges:
            if curr_node is edge.vertex_one and edge.directedness.endswith(">"):
                return edge.vertex_two

            if curr_node is edge.vertex_two and edge.directedness.startswith("<"):
                return edge.vertex_one

        return None

    def has_next(self, node: Node) -> bool:
        return self.get_next(node) is not None

    def get_prev(self, curr_node):
        for edge in self.graph.edges:
            if curr_node is edge.vertex_one and edge.directedness.startswith("<"):
                return edge.vertex_two

            if curr_node is edge.vertex_two and edge.directedness.endswith(">"):
                return edge.vertex_one

        return None

    def add_labeled_pointer(
        self,
        index: int,
        label: str | Element,
        direction: tuple[float, float, float] | None = None,
    ) -> None:
        if isinstance(label, Element):
            label = label.value

        if direction is None:
            direction = -self.head_pointer.direction

        self.labeled_pointers[label] = LabeledLine(
            self.get_node(index),
            label=label,
            direction=direction,
            color=self.color,
        )
        self.add(self.labeled_pointers[label])

    def remove_labeled_pointer(self, label: str | Element) -> None:
        if isinstance(label, Element):
            label = label.value

        self.remove(self.labeled_pointers[label])

    def get_labeled_pointer(self, name: str) -> LabeledLine:
        return self.labeled_pointers[name]

    def move_labeled_pointer(
        self,
        pointer: str | LabeledLine,
        num_nodes: int = 1,
    ) -> tuple[SinglyLinkedList, Animation]:
        copy = self._create_animation_copy()
        copy._move_labeled_pointer(pointer, num_nodes=num_nodes)

        return copy, TransformSinglyLinkedList(
            self,
            copy,
        )

    def _move_labeled_pointer(
        self,
        pointer: str | LabeledLine,
        num_nodes: int = 1,
        pointer_direction=None,
        to: Node | None = None,
    ) -> None:
        if isinstance(pointer, str):
            labeled_pointer = self.get_labeled_pointer(pointer)
        else:
            labeled_pointer = pointer

        if to is None:
            old_node_index: int = self.nodes.index(labeled_pointer.pointee)
            new_node_index: int = old_node_index + num_nodes

            labeled_pointer.shift(
                self.get_node(new_node_index).get_center() - self.get_node(old_node_index).get_center(),
            )
            labeled_pointer.pointee = self.get_node(new_node_index)
        else:
            labeled_pointer.shift(
                to.get_center() - labeled_pointer.pointee.get_center(),
            )
            labeled_pointer.pointee = to

        if pointer_direction is not None:
            labeled_pointer.direction = pointer_direction

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
            ),
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

    def get_next_pointers_node_index(self, pointer: Edge) -> int:
        return [index for index, node in enumerate(self.nodes) if node.next_pointer is pointer][0]

    def _create_animation_copy(self) -> SinglyLinkedList:
        attr_name = "_copy_for_animation"
        if not hasattr(self, attr_name):
            setattr(self, attr_name, self.copy())

        return getattr(self, attr_name)

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

    def insert_node(self, index: int, value, center: bool = True) -> None:
        positive_index = index if index >= 0 else len(self.nodes) + index
        if positive_index < 0 or positive_index > len(self.nodes):
            raise IndexError(f"Index {index} is invalid for length {len(self.nodes)}")

        new_node = self.create_node(value, position_relative_to=(10, 10, 0))

        if self.head is None and self.tail is None:
            self.graph.add_vertex(new_node)
            new_node.move_to(ORIGIN)
            return

        if positive_index == 0:
            self.set_next(new_node, self.head)
        elif positive_index == len(self.nodes):
            self.set_next(self.tail, new_node)
            self.set_next(new_node, self.null)
        else:
            trav = self.head
            trav_index = 0
            while trav_index < (positive_index - 1):
                trav_index += 1
                trav = self.get_next(trav)

            self.set_next(new_node, self.get_next(trav))
            self.set_next(trav, new_node)

        # TODO: I don't think this is needed
        self.graph.add_vertex(new_node)

        trav = self.get_next(self.head)
        while trav is not None:
            # FIXME: Hardcoded relative placement of nodes
            trav.move_to(self.get_prev(trav).get_center() + np.array([RELATIVE_POSITION]))
            trav = self.get_next(trav)

        self.resume_updating()
        self.suspend_updating()

        if center:
            self.move_to(ORIGIN)

    def set_next(self, from_: Node | None, to: Node | None) -> None:
        if self.get_next(from_) == to:
            return

        if self.get_next(from_) is None:
            edge = self.add_edge(from_, to)
        else:
            edge = self.graph.get_edge_from_to(from_, self.get_next(from_))
            if edge.vertex_one == self.get_next(from_):
                edge.vertex_one = to
            else:
                edge.vertex_two = to

            # TODO: Run all unit tests for this
            if to not in self.graph:
                self.graph.add_vertex(to)

        edge.resume_updating()
        edge.suspend_updating()

    def create_node(
        self,
        value,
        position_relative_to,
        position: Iterable[float] = RELATIVE_POSITION,
    ) -> Node:
        SinglyLinkedList._node_counter += 1
        return Node(
            sll=self,
            label=SinglyLinkedList._node_counter,
            contents=value,
            show_label=False,
            position=position,
            position_relative_to=position_relative_to,
            show_container=value != "null",
            container_stroke_width=DEFAULT_STROKE_WIDTH,
            color=self.color,
            radius=DEFAULT_NODE_RADIUS,
            contents_font_size=DEFAULT_FONT_SIZE,
        )

    def add_edge(
        self,
        prev_node,
        next_node,
        quasi: bool = False,
    ) -> Edge:
        return self.graph.add_edge(
            prev_node,
            next_node,
            directedness="->",
            color=self.color,
            line_stroke_width=DEFAULT_STROKE_WIDTH,
            tip_length=DEFAULT_TIP_LENGTH,
            tip_width=DEFAULT_TIP_WIDTH,
            quasi=quasi,
        )


class Node(Vertex):
    def __init__(self, sll: SinglyLinkedList, **kwargs) -> None:
        super().__init__(**kwargs)
        self.sll = sll

    def __repr__(self) -> str:
        return f"Node({self.contents})"

    @property
    def value(self):
        return self.contents

    @property
    def next_pointer(self) -> Edge:
        try:
            return [edge for edge in self.edges if edge.vertex_one is self][0]
        except IndexError:
            pass  # The last node has no next pointer
