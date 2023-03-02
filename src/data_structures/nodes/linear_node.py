from manim import RIGHT, LEFT, Animation, FadeIn, FadeOut

from .node import Node

from ..edges.singly_directed_edge import SinglyDirectedEdge

from typing import Iterable

class LinearNode(Node):
    def __init__(self, shape, data):
        super().__init__(shape, data)
        self._next = None
        self._pointer_to_next = None
        # self._pointer_to_next._is_visible = False

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, node):
        self._next = node

    def get_visible_components(self):
        visible_components = super().get_visible_components()
        if self._pointer_to_next is not None \
        and self._pointer_to_next._is_visible:
            visible_components.append(self._pointer_to_next)

        return visible_components

    def set_next(self, node, add_pointer_to_node = True):
        self.next = node
        # self.next_to(node, LEFT, buff=1)
        self._pointer_to_next = SinglyDirectedEdge(start=self, end=node)
        self.add(self._pointer_to_next)
        self._pointer_to_next._is_visible = True

    def move(self, num_nodes: int) -> Iterable[Animation]:
        animation = self.animate.shift(RIGHT * num_nodes * 2)
        self.shift(RIGHT * num_nodes * 2)
        return animation

    def fade_out_pointer(self) -> None:
        FadeOut(self._pointer_to_next)
        self._pointer_to_next._is_visible = False
    
    def fade_in_pointer(self) -> None:
        FadeIn(self._pointer_to_next)
        self._pointer_to_next._is_visible = True

    def animate_fade_out_pointer(self) -> Animation:
        self._pointer_to_next._is_visible = False
        return FadeOut(self._pointer_to_next)

    def animate_fade_in_pointer(self) -> Animation:
        self.add(self._pointer_to_next)
        self._pointer_to_next._is_visible = True
        return FadeIn(self._pointer_to_next)

    def get_next_pointer_top(self):
        return self._pointer_to_next.get_top()

    def get_next_pointer_right(self):
        return self._pointer_to_next.get_right()

    def get_next_pointer_bottom(self):
        return self._pointer_to_next.get_bottom()

    def get_next_pointer_left(self):
        return self._pointer_to_next.get_left()