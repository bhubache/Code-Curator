from manim import RIGHT, LEFT, Animation, FadeIn

from .node import Node

from ..edges.singly_directed_edge import SinglyDirectedEdge

from typing import Iterable

class LinearNode(Node):
    def __init__(self, shape, data):
        super().__init__(shape, data)
        self._next = None
        self._pointer_to_next = None

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, node):
        self._next = node

    def set_next(self, node, add_pointer_to_node = True):
        self.next = node
        # self.next_to(node, LEFT, buff=1)
        self._pointer_to_next = SinglyDirectedEdge(start=self, end=node)
        self.add(self._pointer_to_next)

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