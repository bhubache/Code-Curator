from __future__ import annotations

from collections.abc import Iterable

from code_curator.custom_vmobject import CustomVMobject
from manim import Animation
from manim import RIGHT

from ..edges.singly_directed_edge import SinglyDirectedEdge
from .node import Node


class LinearNode(Node):
    def __init__(
        self,
        data: float | str,
        /,
        *,
        shape: CustomVMobject,
    ) -> None:
        super().__init__(data, shape=shape)
        self.next: LinearNode | None = None
        self.pointer_to_next: SinglyDirectedEdge | None = None

    def set_next(self, node: LinearNode):
        self.next = node

        # Remove the existing pointer (if it exists) from the screen
        if self.pointer_to_next is not None:
            self.remove(self.pointer_to_next)
        # self.next_to(node, LEFT, buff=1)
        if self.pointer_to_next is None:
            self.pointer_to_next = SinglyDirectedEdge(start=self, end=node)
        else:

            # TEST!!!
            if self._diagonal_with_other(node):
                self.pointer_to_next.become(
                    SinglyDirectedEdge(
                        start=self.get_container_right(),
                        end=node.get_container_left(),
                    ),
                )
            else:
                self.pointer_to_next.become(
                    SinglyDirectedEdge(
                        start=self,
                        end=node,
                    ),
                )

        self.add(self.pointer_to_next)

        # NOTE: TEST!!!
        # return self.pointer_to_next
        return self, self.pointer_to_next

    def _diagonal_with_other(self, other: LinearNode) -> bool:
        diff = self.get_container_center() - other.get_container_center()
        return diff[0] != 0.0 and diff[1] != 0.0

    def move(self, num_nodes: int) -> Iterable[Animation]:
        animation = self.animate.shift(RIGHT * num_nodes * 2)
        self.shift(RIGHT * num_nodes * 2)
        return animation

    def get_next_pointer_top(self):
        return self.pointer_to_next.get_top()

    def get_next_pointer_right(self):
        return self.pointer_to_next.get_right()

    def get_next_pointer_bottom(self):
        return self.pointer_to_next.get_bottom()

    def get_next_pointer_left(self):
        return self.pointer_to_next.get_left()
