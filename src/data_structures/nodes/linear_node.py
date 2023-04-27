from __future__ import annotations

from collections.abc import Iterable

from manim import Animation
from manim import RIGHT

from ..edges.singly_directed_edge import SinglyDirectedEdge
from .node import Node
from src.custom_vmobject import CustomVMobject


class LinearNode(Node):
    def __init__(self, data: float | str, shape: CustomVMobject):
        super().__init__(data, shape)
        self._next = None
        self._pointer_to_next = None

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, node):
        self._next = node

    def set_next(self, node: LinearNode):
        self.next = node

        # Remove the existing pointer (if it exists) from the screen
        if self._pointer_to_next is not None:
            self.remove(self._pointer_to_next)
        # self.next_to(node, LEFT, buff=1)
        if self._pointer_to_next is None:
            self._pointer_to_next = SinglyDirectedEdge(start=self, end=node)
        else:

            # TEST!!!
            if self._diagonal_with_other(node):
                self._pointer_to_next.become(
                    SinglyDirectedEdge(
                        start=self.get_container_right(),
                        end=node.get_container_left(),
                    ),
                )
            else:
                self._pointer_to_next.become(
                    SinglyDirectedEdge(
                        start=self,
                        end=node,
                    ),
                )

        self.add(self._pointer_to_next)

        # NOTE: TEST!!!
        # return self.pointer_to_next
        return self, self._pointer_to_next

    def _diagonal_with_other(self, other: LinearNode) -> bool:
        diff = self.get_container_center() - other.get_container_center()
        return diff[0] != 0.0 and diff[1] != 0.0

    def move(self, num_nodes: int) -> Iterable[Animation]:
        animation = self.animate.shift(RIGHT * num_nodes * 2)
        self.shift(RIGHT * num_nodes * 2)
        return animation

    def get_next_pointer_top(self):
        return self._pointer_to_next.get_top()

    def get_next_pointer_right(self):
        return self._pointer_to_next.get_right()

    def get_next_pointer_bottom(self):
        return self._pointer_to_next.get_bottom()

    def get_next_pointer_left(self):
        return self._pointer_to_next.get_left()

    @property
    def pointer_to_next(self):
        return self._pointer_to_next
