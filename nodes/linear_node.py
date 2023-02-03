from manim import *

from .node import Node

from edges.singly_directed_edge import SinglyDirectedEdge

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

    def set_next(self, node, add_pointer_to_screen = False):
        self.next = node
        self._pointer_to_next = SinglyDirectedEdge(start=self, end=node)
        if add_pointer_to_screen:
            self.add(self._pointer_to_next)
        return [FadeIn(self._pointer_to_next)]

    def move(self, num_nodes: int) -> Iterable[Animation]:
        animation = self.animate.shift(RIGHT * num_nodes * 2)
        self.shift(RIGHT * num_nodes * 2)
        return animation

    def get_node_bottom(self):
        if self._pointer_to_next is None:
            return self.get_bottom()
        
        self.remove(self._pointer_to_next)
        bottom = self.get_bottom()
        self.add(self._pointer_to_next)
        return bottom

    def get_node_top(self):
        if self._pointer_to_next is None:
            return self.get_top()
        
        self.remove(self._pointer_to_next)
        bottom = self.get_top()
        self.add(self._pointer_to_next)
        return bottom