from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from manim import Animation
from manim import DOWN
from manim import Mobject
from manim import ORIGIN
from manim import UP
from manim import WHITE
from manim.mobject.mobject import _AnimationBuilder

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
    from manim.typing import Vector
    import types

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
        self._head: Node | None = None

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
        if self._head is None:
            return None

        trav = self._head
        while self.get_prev(trav) is not None:
            trav = self.get_prev(trav)

        self._head = trav
        return self._head

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
        if self.head is None:
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
            return self.graph.labeled_pointers["head"]
        except LookupError:
            return None

    @property
    def tail_pointer(self) -> LabeledLine | None:
        try:
            return self.graph.labeled_pointers["tail"]
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

    @property
    def animate(self) -> AnimationBuilder:
        return AnimationBuilder(self)

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

        if self._head is None:
            self._head = self.null

        return self

    def remove_null(self):
        raise NotImplementedError()
        return self

    def add_head_pointer(self, center: bool = True):
        if not self.has_head:
            raise RuntimeError("Unable to add head pointer because no head is present")

        self.graph.add_labeled_pointer(
            self.head,
            label="head",
            direction=DOWN,
            color=self.color,
        )

        self.add_updater(self.head_pointer_updater, call_updater=True)

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

        self.graph.add_labeled_pointer(
            self.tail,
            label="tail",
            direction=tail_direction,
            color=self.color,
        )

        self.add_updater(self.tail_pointer_updater, call_updater=True)

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

    def remove(self, *mobjects: Mobject):
        for mob in mobjects:
            if isinstance(mob, (Vertex, Edge)):
                self.graph.remove(mob)
            else:
                raise NotImplementedError(f"Removal of mobject {mob} from SLL not yet supported")

    def get_node(self, index: int) -> Node:
        return self.nodes[index]

    def get_node_index(self, node: Node) -> int:
        return self.nodes.index(node)

    def get_next_pointer(self, node: Node) -> Edge:
        return self.graph.get_edge_from_to(node, self.get_next(node))

    def get_next(self, curr_node):
        for edge in self.graph.edges:
            if curr_node is edge.vertex_one and edge.directedness.endswith(">"):
                return edge.vertex_two

            if curr_node is edge.vertex_two and edge.directedness.startswith("<"):
                return edge.vertex_one

        return None

    def has_next(self, node: Node) -> bool:
        return self.get_next(node) is not None

    # TODO: Tests
    def set_next(self, from_: Node | None, to: Node | None, angle_in_degrees: float = 0.0) -> None:
        if self.get_next(from_) == to:
            return

        if self.get_next(from_) is None:
            edge = self.add_edge(from_, to, angle_in_degrees=angle_in_degrees)
        else:
            edge = self.graph.get_edge_from_to(from_, self.get_next(from_))
            edge.reconnect(self.get_next(from_), to, angle_in_degrees)

            # TODO: Run all unit tests for this
            if to not in self.graph:
                self.graph.add_vertex(to)

        edge.force_update()

    def get_prev(self, curr_node):
        for edge in self.graph.edges:
            if curr_node is edge.vertex_one and edge.directedness.startswith("<"):
                return edge.vertex_two

            if curr_node is edge.vertex_two and edge.directedness.endswith(">"):
                return edge.vertex_one

        return None

    # FIXME: Appears immediately on screen at end of animation rather than fading in
    def add_labeled_pointer(
        self,
        to: Node,
        label: str | Element,
        direction: tuple[float, float, float] | None = None,
        center: bool = True,
    ) -> None:
        if direction is None:
            direction = -self.head_pointer.direction

        self.graph.add_labeled_pointer(
            to,
            label=label,
            direction=direction,
            color=self.color,
        )

        if center:
            self.move_to(ORIGIN)

    def remove_labeled_pointer(self, label: str | Element) -> None:
        if isinstance(label, Element):
            label = label.value

        self.remove(self.labeled_pointers[label])

    def get_labeled_pointer(self, name: str) -> LabeledLine:
        return self.labeled_pointers[name]

    def move_labeled_pointer(
        self,
        pointer: str | LabeledLine,
        to: Node,
        pointer_direction: Vector | None = None,
    ) -> None:
        if isinstance(pointer, str):
            labeled_pointer = self.get_labeled_pointer(pointer)
        else:
            labeled_pointer = pointer

        labeled_pointer.pointee = to

        if pointer_direction is not None:
            labeled_pointer.direction = pointer_direction

        labeled_pointer.force_update()

    def shrink_pointer(self, pointer: Edge) -> tuple[SinglyLinkedList, Animation]:
        node_index: int = self.get_next_pointers_node_index(pointer)

        copy = self._create_animation_copy()
        start = self.get_node(node_index).next_pointer.get_start()
        copy.get_node(node_index).next_pointer.put_start_and_end_on(start, start)
        return copy, TransformSinglyLinkedList(
            self,
            copy,
        )

    def flatten(self, center: bool = True) -> None:
        if self.has_head:
            trav = self.get_next(self.head)
            while trav is not None:
                # FIXME: Hardcoded relative placement of nodes
                trav.move_to(self.get_prev(trav).get_center() + np.array([RELATIVE_POSITION]))
                trav = self.get_next(trav)

        if center:
            self.move_to(ORIGIN)

        self.force_update()

    def get_next_pointers_node_index(self, pointer: Edge) -> int:
        return [index for index, node in enumerate(self.nodes) if node.next_pointer is pointer][0]

    def insert_node(self, index: int, value, center: bool = True) -> None:
        positive_index = index if index >= 0 else len(self.nodes) + index
        if positive_index < 0 or positive_index > len(self.nodes):
            raise IndexError(f"Index {index} is invalid for length {len(self.nodes)}")

        new_node = self.create_node(value)

        if self.head is None and self.tail is None:
            self._head = new_node
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

        self.flatten(center=center)

    def create_node(
        self,
        value,
        position_relative_to: Mobject | None = None,
        position: Iterable[float] = RELATIVE_POSITION,
    ) -> Node:
        SinglyLinkedList._node_counter += 1

        if position_relative_to is None:
            position_relative_to = ORIGIN

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
        angle_in_degrees: float = 0.0,
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
            angle_in_degrees=angle_in_degrees,
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


class AnimationBuilder(_AnimationBuilder):
    def __getattr__(self, method_name) -> types.MethodType:
        method = getattr(self.mobject.target, method_name)
        has_overridden_animation = hasattr(method, "_override_animate")

        if (self.is_chaining and has_overridden_animation) or self.overridden_animation:
            raise NotImplementedError(
                "Method chaining is currently not supported for overridden animations",
            )

        def update_target(*method_args, **method_kwargs):
            if has_overridden_animation:
                self.overridden_animation = method._override_animate(
                    self.mobject,
                    *method_args,
                    anim_args=self.anim_args,
                    **method_kwargs,
                )
            else:
                self.methods.append([method, method_args, method_kwargs])
                # TODO: In the example of move_labeled_pointer, we pass in the labeled_pointer to move.
                #  This comes from self.mobject, which is an issue because the method is being applied to
                #  self.mobject.target. So, for any arg and kwarg passed in that's from self.mobject, we
                #  need to replace it with the equivalent from self.mobject.target

                method_args_with_target_submobjects = []

                for positional_arg in method_args:
                    if not isinstance(positional_arg, Mobject):
                        method_args_with_target_submobjects.append(positional_arg)
                        continue

                    # TODO: Learn what ``get_family`` is doing
                    for target_sm in self.mobject.target.get_family():
                        try:
                            if target_sm.original_id == str(id(positional_arg)):
                                method_args_with_target_submobjects.append(target_sm)
                        except AttributeError:
                            continue  # sm in target is new and thus not present in self.mobject

                for key, value in method_kwargs.items():
                    if not isinstance(value, Mobject):
                        continue

                    # TODO: Learn what ``get_family`` is doing
                    for target_sm in self.mobject.target.get_family():
                        try:
                            if target_sm.original_id == str(id(value)):
                                method_kwargs[key] = target_sm
                        except AttributeError:
                            continue  # sm in target is new and thus not present in self.mobject

                method(*method_args_with_target_submobjects, **method_kwargs)

            return self

        self.is_chaining = True
        self.cannot_pass_args = True

        return update_target

    def build(self) -> Animation:
        if self.overridden_animation:
            anim = self.overridden_animation
        else:
            self.mobject.suspend_updating()
            anim = TransformSinglyLinkedList(self.mobject, self.methods)

        for attr, value in self.anim_args.items():
            setattr(anim, attr, value)

        return anim
