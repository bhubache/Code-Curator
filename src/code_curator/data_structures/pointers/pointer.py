from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

import numpy as np
from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.data_structures.static_array_parts.values.element import Element
from manim import Animation
from manim import AnimationGroup
from manim import DOWN
from manim import Line
from manim import UP

from ..edges.singly_directed_edge import SinglyDirectedEdge
from ..nodes.node import Node
from .base_pointer import BasePointer
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from ..singly_linked_list import SinglyLinkedList


class Pointer(SinglyDirectedEdge, BasePointer):
    def __init__(
        self,
        node: Node,
        sll: SinglyLinkedList,
        label=None,
        direction=DOWN,
        start=None,
        end=None,
        tip_shape=None,
    ) -> None:
        self._sll = sll
        # TODO: More fleshed out implementation for where the pointer starts and ends
        relative_placement = None
        if end is None:
            if self.lists_equal(direction, DOWN):
                relative_placement = node.get_container_top.__func__
                end = node.get_container_top()

            elif self.lists_equal(direction, UP):
                relative_placement = node.get_container_bottom.__func__
                end = node.get_container_bottom()
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

        self._label.next_to(self, self.opposite_of_direction())
        self.add(self._label)

    def get_label(self) -> Element:
        return self._label

    def lists_equal(self, a: list, b: list) -> bool:
        if len(a) != len(b):
            return False

        for e1, e2 in zip(a, b):
            if e1 != e2:
                return False
        return True

    @property
    def node(self):
        return self._node

    # def move(self, positioned_node, actual_node) -> Iterable[Animation]:
    #     self._node = actual_node
    #     if self._node not in self._sll.submobjects:
    #         raise
    #     relative_location = self._relative_placement(positioned_node)
    #     start = [
    #         relative_location[0], relative_location[1] +
    #         (self.vertical_length * -self._direction[1]), 0,
    #     ]
    #     return AnimationGroup(
    #         self.animate.put_start_and_end_on(start, relative_location),
    #     )

    # TODO: Use vectors to make this generalized to all directions
    def move_immediately_alpha(self, positioned_node, actual_node, alpha) -> None:
        self._node = actual_node

        start, end = self.get_start_and_end()
        line = Line(start=end, end=self._relative_placement(positioned_node))
        new_end = line.point_from_proportion(alpha)
        self.put_start_and_end_on(new_end + (self.start - self.end), new_end)

    def get_opposite_direction(self):
        return np.array([self._direction[0], self._direction[1] * -1, self._direction[2]])

    # FIXME: VERY VERY basic
    def opposite_of_direction(self):
        return np.array([self._direction[0], self._direction[1] * -1, self._direction[2]])
