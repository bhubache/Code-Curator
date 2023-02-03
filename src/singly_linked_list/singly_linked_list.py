from manim import *

from nodes.singly_linked_list_node import SLLNode as Node
from pointers.pointer import Pointer
from edges.singly_directed_edge import SinglyDirectedEdge

from typing import Iterable

import inspect

def create_sll(data_list):
    return SinglyLinkedList(*data_list)


class SinglyLinkedList(VMobject):
    def __init__(self, *elements, shape = None):
        super().__init__()
        self._nodes = []
        self._head = None
        self._tail = None

        trav = None
        for i, elem in enumerate(elements):
            node = Node(elem)
            if i == 0:
                self._head = node
                trav = self._head
            else:
                self._place_node_next_to(node, trav)
                trav.set_next(node, add_pointer_to_screen=True)
                if i == len(elements) - 1:
                    self._tail = node

                trav = trav.next

            self._nodes.append(node)
            self.add(node)

        self._head_pointer = Pointer(self._head, 'head', DOWN)
        self._tail_pointer = Pointer(self._tail, 'tail', DOWN)

        self.add(self._head_pointer)
        self.add(self._tail_pointer)

        self.move_to([0, 0, 0])

    def append(self, data) -> Iterable[Animation]:
        return self.add_last(data)

    # NOTE: 1/22/2023
    # self._nodes.append(node) moved above animation appends to see if self._move_pointer is fixed
    def add_last(self, data) -> Iterable[Animation]:
        node = Node(data)
        self.add(node)
        self._place_node_next_to(node, self._tail)
        self._tail.set_next(node)

        self._nodes.append(node)

        animations = []
        animations.append(AnimationGroup(FadeIn(self._tail._pointer_to_next), FadeIn(node)))
        animations.append(self.animate.move_to([0, 0, 0]))
        animations.append(self._move_pointer(self._tail_pointer, 1))
        self._tail = node

        # self._nodes.append(node)
        return animations

    def prepend(self, data) -> Iterable[Animation]:
        return self.add_first(data)

    def add_first(self, data) -> Iterable[Animation]:
        node = Node(data)
        self.add(node)
        self._place_node_next_to(node, self._head, LEFT)
        node.set_next(self._head)

        animations = []
        animations.append(FadeIn(node))
        animations.append(self.animate.move_to([0, 0, 0]))
        animations.append(self._move_pointer(self._head_pointer, -1))
        self._head = node

        self._nodes.insert(0, node)
        return animations

    def insert_at_index(self, index: int, data) -> Iterable[Animation]:
        trav = Pointer(self._head, 'trav', UP)

        animations = []
        animations.append(AnimationGroup(*(FadeIn(trav), self.animate.move_to([0, 0, 0]))))
        animations.append(self.animate.move_to([0, 0, 0]))

        trav_shifts = []
        num_to_shift = index - 1
        # animations += Succession()
        # for i in range(num_to_shift):
        animations += [Succession(*[self._move_pointer(trav, 1) for _ in range(num_to_shift)])]
            # trav_shifts.append(self._move_pointer(trav, 1))
            # trav_shifts.append(AnimationGroup(self._move_pointer(trav, 1)))
        # animations += Succession(*trav_shifts)
        # animations += trav_shifts


        new_node = Node(data)
        # new_node.next_to(trav, RIGHT, aligned_edge=trav.get_bottom())

        #FIXME: This may get out of bounds
        # new_node.next_to(self._nodes[num_to_shift + 1], aligned_edge=self._nodes[num_to_shift + 1].get_bottom())
        new_node.move_to(trav.get_bottom())
        new_node.move(1)
        # self._move_pointer(new_node, 1)
        animations.append(AnimationGroup(FadeIn(new_node)))

        new_node.set_next(self._nodes[index])
        animations.append(AnimationGroup(FadeIn(new_node._pointer_to_next)))

        trav_node = self._nodes[num_to_shift]
        # animations.append(AnimationGroup(trav_node._pointer_to_next.animate.put_start_and_end_on(start=trav_node._pointer_to_next.get_left(), end=new_node.get_left())))

        trav_node._pointer_to_next.generate_target()
        trav_node._pointer_to_next.target = SinglyDirectedEdge(start=trav_node._pointer_to_next.get_left(), end=new_node.get_left())
        animations.append(AnimationGroup(MoveToTarget(trav_node._pointer_to_next)))

        self._nodes.insert(index, new_node)
        animations.append(AnimationGroup(*self._flatten()))

        # animations.append(AnimationGroup(MoveToTarget(self)))



        # Reset trav back to head so the trav shift animations proceed as expected
        self._move_pointer(trav, -num_to_shift)
        return animations

    def remove_at_inex(self):
        pass

    def remove(self):
        pass

    

    # FIXME: Hardcoded shift value
    # NOTE: Has the side effect of moving the pointer on the scene without the animation as well
    def _move_pointer(self, pointer: Pointer, num_nodes: int) -> Iterable[Animation]:
        return pointer.move(num_nodes, self._nodes[self._index_of_pointer(pointer) + num_nodes])

    def _index_of_pointer(self, pointer):
        return self._nodes.index(pointer.node)

    def _place_node_next_to(self, node, other, direction = RIGHT, buff = 1):
        node.next_to(other, direction, buff = buff)

    def _flatten(self):
        data_list = [node._data for node in self._nodes]
        flattened_copy = create_sll(data_list)
        
        animations = []
        for self_node, flattened_node in zip(self._nodes, flattened_copy._nodes):
            animations.append(self_node.animate.move_to(flattened_node))
        # animations.append(self.animate.move_to([0, 0, 0]))
        return animations