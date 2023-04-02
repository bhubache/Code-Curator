from __future__ import annotations
import math

from typing import Iterable, Any

from ..nodes.singly_linked_list_node import SLLNode
from ..pointers.pointer import Pointer
from ..edges.singly_directed_edge import SinglyDirectedEdge
from animations.singly_linked_list.subanimations.fade_in_container import FadeInContainer
# from animations.singly_linked_list.subanimations.fade_in_pointer import FadeInPointer
from animations.singly_linked_list.subanimations.grow_pointer import GrowPointer
from animations.singly_linked_list.subanimations.move_trav import MoveTrav
from animations.singly_linked_list.subanimations.center_sll import CenterSLL
# from animations.singly_linked_list.add_first import AddFirst
# from animations.singly_linked_list.add_last import AddLast
# from animations.singly_linked_list.remove_first import RemoveFirst
# from animations.singly_linked_list.remove_last import RemoveLast
# from animations.singly_linked_list.insert import Insert
from animations.singly_linked_list.remove_at import RemoveAt
from manim import VMobject, DOWN, LEFT, UP, RIGHT, FadeIn, FadeOut, Animation, AnimationGroup, Succession, UpdateFromAlphaFunc, VGroup

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

# The following imports are for development
# from animations.singly_linked_list.subanimations.fade_in_pointer import FadeInPointer
from animations.singly_linked_list.subanimations.fade_in_container import FadeInContainer
# from animations.animation_package import AnimationPackage
from animations.data_structure_animation import DataStructureAnimation
import sys

# TODO: Consider using the builder design pattern rather than including for every possible subanimation combination out of the box


def create_sll(data_list):
    return SinglyLinkedList(*data_list)

# TODO: A lot of duplicate code that needs to be removed.


class SinglyLinkedList(VMobject):
    def __init__(self, *elements: list[Any], shape = None) -> None:
        super().__init__()
        self._elements = elements
        self._nodes = []
        self._head = None
        self._tail = None
        self._saved_states = {}
        # self._animation_package = AnimationPackage(self)

        if len(elements) == 0:
            raise AttributeError('Linked List cannot have zero elements')

        for i in range (1, len(elements)):
            prev = None
            if i == 1:
                prev = SLLNode(elements[i - 1])
                self._head = prev
                self._nodes.append(prev)
                self.add(prev)
            else:
                prev = self._nodes[i - 1]

            curr = SLLNode(elements[i])

            self._place_node_next_to(curr, prev, RIGHT)
            prev.set_next(curr)

            if i == len(elements) - 1:
                self._tail = curr

            self._nodes.append(curr)
            self.add(curr)

        self.head_pointer = Pointer(self._head, self, 'head', DOWN)
        self.tail_pointer = None
        if len(elements) == 1:
            self.tail_pointer = Pointer(self._tail, self, 'tail', UP)
        elif len(elements) > 1:
            self.tail_pointer = Pointer(self._tail, self, 'tail', DOWN)

        self.add(self.head_pointer)
        self.add(self.tail_pointer)

        self.move_to([0, 0, 0])

    def __getitem__(self, index: int) -> SLLNode:
        return self._nodes[index]

    def __setitem__(self, index: int, value: SLLNode) -> None:
        self._nodes[index] = value

    def __iter__(self):
        return self._nodes.__iter__()

    def __len__(self):
        return len(self._nodes)

    @staticmethod
    def create_sll(sll: SinglyLinkedList) -> SinglyLinkedList:
        return SinglyLinkedList(*[node.data._value for node in sll])

    def insert(
        self,
        index: int,
        data: Any,
        display_first_trav: bool = False,
        first_trav_name: str = 'p1',
        display_second_trav: bool = False,
        second_trav_name: str = 'p2',
        trav_position: str = 'start',
        aligned: bool = False,
        **kwargs
    ) -> Insert:
        return Insert.create_packager(
            sll=self,
            index=index,
            data=data,
            node=self._add_node(index, data, aligned=aligned),
            display_first_trav=display_first_trav,
            first_trav_name=first_trav_name,
            display_second_trav=display_second_trav,
            second_trav_name=second_trav_name,
            trav_position=trav_position,
            aligned=aligned,
            sll_calling_method=self.insert
        )

    def remove_at(
        self,
        index: int,
        display_first_trav: bool = False,
        first_trav_name: str = 'p1',
        display_second_trav: bool = False,
        second_trav_name: str = 'p2',
        trav_position: str = 'start',
        aligned: bool = False,
        **kwargs
    ) -> RemoveAt:
        return RemoveAt.create_packager(
            sll=self,
            index=index,
            node=self._remove_node(index),
            display_first_trav=display_first_trav,
            first_trav_name=first_trav_name,
            display_second_trav=display_second_trav,
            second_trav_name=second_trav_name,
            trav_position=trav_position,
            aligned=aligned,
            sll_calling_method=self.remove_at
        )

    # NOTE: Maybe also remove node from sll?
    # NOTE: Can't remove the node from self._nodes yet
    # TODO: Change node's next attribute!!!!
    def _remove_node(self, index: int) -> SLLNode:
        if index < 0:
            index = len(self) + index

        if index >= len(self):
            raise IndexError(f'Index {index} out of bounds for length {len(self)}')

        node = self[index]
        # del self._nodes[index]
        # del self[index]

        if index == 0:
            self._head = self[1]
        if index == len(self) - 1:
            self._tail = self[-2]

        return node

    # TODO: Change node's next attribute!!!!
    def _add_node(self, index: int, data: Any, aligned: bool = True) -> SLLNode:
        if index < 0:
            index = len(self) + index

        if index > len(self):
            raise IndexError(f'Index {index} out of bounds for length {len(self)}')

        node = SLLNode(data)
        self._nodes.insert(index, node)
        if index == 0:
            self._head = node
        if index == len(self):
            self._tail = node

        # TODO: Adjust all of these because the node is not yet inserted!!!
        if index == 0:
            if aligned:
                # node.next_to(self[1].container, LEFT, buff=(self[1].pointer_to_next.length + (2 * self[1].container.radius)))
                # node.next_to(self[1].container, LEFT, buff=0)
                node.align_to(self[1].container, LEFT + DOWN)
                node.shift(LEFT * ((self[0].radius * 2) + self[1].pointer_to_next.length))
                node.set_next(self[1])
            else:
                raise NotImplementedError('Nonaligned insertion of a node at the front of linked list is not yet supported')
        elif index < len(self) - 1:
            if aligned:
                node.next_to(self[index - 1], RIGHT, buff=0)

                # Visually place the node in the correct spot on the screen
                # NOTE: Side effect of setting the node's next node 1 too far
                node.set_next(self[index + 2])

                # Set the node's next node to the correct node
                node.next = self[index + 1]
            else:
                node.next_to(self[index + 1].container, DOWN)
                node.set_next(self[index + 1])
        else:
            node.next_to(self[-2], RIGHT, buff=self[0].pointer_to_next.length)
            self[-2].set_next(node)
            self[-2].pointer_to_next.set_opacity(0)

            if not aligned:
                node.shift(DOWN)
                self[-2].pointer_to_next.become(SinglyDirectedEdge(start=self[-2].pointer_to_next.start, end=node.get_container_left()))

        if node.pointer_to_next is not None:
            node.add(node.pointer_to_next)
        node.add(node.container)
        self.add(node)

        return node

    # FIXME: Hardcoded shift value
    # NOTE: Has the side effect of moving the pointer on the scene without the animation as well
    def _move_pointer(self, pointer: Pointer, positioned_node, actual_node) -> Iterable[Animation]:
        return pointer.move(positioned_node, actual_node)
        # return pointer.move(num_nodes, self._nodes[self._index_of_pointer(pointer) + num_nodes])

    def _immediately_move_pointer(self, pointer: Pointer, positioned_node, actual_node) -> None:
        pointer.immediately_move(positioned_node, actual_node)

    def _index_of_pointer(self, pointer):
        return self._nodes.index(pointer.node)

    # FIXME: Hard coded buff
    def _place_node_next_to(self, node, other, direction = RIGHT, buff = 1):
        node.next_to(other, direction, buff = buff)
