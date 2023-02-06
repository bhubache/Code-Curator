from manim import DOWN, RIGHT

from ..edges.singly_directed_edge import SinglyDirectedEdge
from data_structures.static_array_parts.values.element import Element

from typing import Iterable
import numpy as np

class Pointer(SinglyDirectedEdge):
    def my_closure(self, node):
        def position_updater(self):
            location = node.get_node_bottom() if self._direction[1] == 1 else node.get_node_top()
            self.next_to(location, opposite_of_direction(self._direction), buff=0)

            # location = self._node.get_node_bottom() if self._direction[1] == 1 else self._node.get_node_top()
            # self.next_to(location, opposite_of_direction(self._direction), buff=0)
        return position_updater

    def __init__(self, node, label = None, direction = DOWN, start = None, end = None, tip_shape = None):
        # TODO: More fleshed out implementation for where the pointer starts and ends
        self._node = node
        self._node_list = [self._node]
        self._direction = direction
        end = end if end is not None else self._node.get_node_bottom()
        if self._direction[1] == -1:
            end = self._node.get_node_top()
            
        start_x = end[0]
        start_y = end[1] - 1.25
        if self._direction[1] == -1:
            start_y = end[1] + 1.25
        start_z = end[2]
        start = start if start is not None else [start_x, start_y, start_z]
        super().__init__(start=start, end=end, tip_shape=tip_shape)
        self._label = Element(label)
        
        self._label.next_to(self, opposite_of_direction(self._direction))
        self.add(self._label)

        # def my_closure(self, node):
        #     def position_updater(self):
        #         location = node.get_node_bottom() if self._direction[1] == 1 else node.get_node_top()
        #         self.next_to(location, opposite_of_direction(self._direction), buff=0)

        #         # location = self._node.get_node_bottom() if self._direction[1] == 1 else self._node.get_node_top()
        #         # self.next_to(location, opposite_of_direction(self._direction), buff=0)
        #     return position_updater

        # self.add_updater(position_updater)
        self.add_updater(self.my_closure(self._node))

    @property
    def node(self):
        return self._node

    def move(self, num_nodes: int, node) -> Iterable[Animation]:
        # self.suspend_updating()
        self.remove_updater(self.my_closure(self._node))
        self._node = node
        # self.resume_updating()
        animation = self.animate.shift(RIGHT * num_nodes * 2)
        self.shift(RIGHT * num_nodes * 2)
        # self.resume_updating()
        self.add_updater(self.my_closure(node))
        return animation

# FIXME: VERY VERY basic
def opposite_of_direction(direction):
    return np.array([direction[0], direction[1] * -1, direction[2]])