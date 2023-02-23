from manim import DOWN, RIGHT, LEFT, UP, Animation, RED, YELLOW, AnimationGroup, Create, Circle, FadeOut

from ..edges.singly_directed_edge import SinglyDirectedEdge
from data_structures.static_array_parts.values.element import Element

from typing import Iterable
import numpy as np

class Pointer(SinglyDirectedEdge):
    # def my_closure(self, node):
    #     def position_updater(self):
    #         location = node.get_node_bottom() if self._direction[1] == 1 else node.get_node_top()
    #         self.next_to(location, opposite_of_direction(self._direction), buff=0)

    #         # location = self._node.get_node_bottom() if self._direction[1] == 1 else self._node.get_node_top()
    #         # self.next_to(location, opposite_of_direction(self._direction), buff=0)
    #     return position_updater

    def lists_equal(self, a: list, b: list) -> bool:
        if len(a) != len(b): return False

        for e1, e2 in zip(a, b):
            if e1 != e2: return False
        return True

    def __init__(self, node, label = None, direction = DOWN, start = None, end = None, tip_shape = None):
        # TODO: More fleshed out implementation for where the pointer starts and ends
        relative_placement = None
        if end is None:
            if self.lists_equal(direction, DOWN):
                relative_placement = node.get_node_top.__func__
                end = node.get_node_top()

            elif self.lists_equal(direction, UP):
                relative_placement = node.get_node_bottom.__func__
                end = node.get_node_bottom()
            else:
                raise NotImplementedError()
        start_x = end[0]
        start_y = end[1] - (node.radius * 2)
        # start_y = end[1] - 1.25
        if direction[1] == -1:
            start_y = end[1] + (node.radius * 2)
            # start_y = end[1] + 1.25
        start_z = end[2]
        start = start if start is not None else [start_x, start_y, start_z]
        
        super().__init__(start=start, end=end, tip_shape=tip_shape)

        self._node = node
        self._relative_placement = relative_placement
        self._direction = direction
        
        self._label = Element(label)
        
        self._label.next_to(self, opposite_of_direction(self._direction))
        self.add(self._label)

    @property
    def node(self):
        return self._node

    def move(self, positioned_node, actual_node) -> Iterable[Animation]:
        self._node = actual_node
        relative_location = self._relative_placement(positioned_node)
        start = [relative_location[0], relative_location[1] + self.vertical_length, 0]
        return AnimationGroup(
            self.animate.put_start_and_end_on(start, relative_location)
        )


# FIXME: VERY VERY basic
def opposite_of_direction(direction):
    return np.array([direction[0], direction[1] * -1, direction[2]])