from manim import VMobject, DOWN, LEFT, UP, RIGHT, FadeIn, FadeOut, Animation, AnimationGroup, Succession, UpdateFromAlphaFunc, Circle

from ..nodes.singly_linked_list_node import SLLNode as Node
from ..pointers.pointer import Pointer
from ..edges.singly_directed_edge import SinglyDirectedEdge

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

        for i in range (1, len(elements)):
            prev = None
            if i == 1:
                prev = Node(elements[i - 1])
                self._head = prev
                self._nodes.append(prev)
                self.add(prev)
            else:
                prev = self._nodes[i - 1]

            curr = Node(elements[i])

            self._place_node_next_to(curr, prev, RIGHT)
            prev.set_next(curr)

            if i == len(elements) - 1:
                self._tail = curr

            self._nodes.append(curr)
            self.add(curr)

        self._head_pointer = Pointer(self._head, 'head', DOWN)
        self._tail_pointer = None
        if len(elements) == 1:
            self._tail_pointer = Pointer(self._tail, 'tail', UP)
        elif len(elements) > 1:
            self._tail_pointer = Pointer(self._tail, 'tail', DOWN)

        self.add(self._head_pointer)
        self.add(self._tail_pointer)

        self.move_to([0, 0, 0])

        # for node in self._nodes:
        #     node.remove(node._pointer_to_next)
        #     if node._pointer_to_next is not None:
        #         self.add(node._pointer_to_next)

    def append(self, data) -> Iterable[Animation]:
        return self.add_last(data)

    # NOTE: 1/22/2023
    # self._nodes.append(node) moved above animation appends to see if self._move_pointer is fixed
    def add_last(self, data, num_animations: int) -> Iterable[Animation]:
        node = Node(data)
        self._place_node_next_to(node, self._tail)
        self._tail.set_next(node)
        self.add(node)
        FadeOut(node)

        # self.add(self._tail._pointer_to_next)
        # FadeOut(self._tail._pointer_to_next)

        self._nodes.append(node)

        def update_sll(mobject, alpha):
            self._nodes[len(self._nodes) - 2]._pointer_to_next.fade(1 - alpha)
            node.fade(1 - alpha)


        # NOTE THIS WAS HERE
        # NOTE: This may not be correct
        self._tail = node

        AnimationTiming = None
        if num_animations == 1:
            AnimationTiming = AnimationGroup
        elif num_animations == 2:
            AnimationTiming = Succession
        else:
            raise NotImplementedError()

        return AnimationTiming(AnimationGroup(
            self.animate.move_to([0, 0, 0]),
            UpdateFromAlphaFunc(self, update_sll)
        ),
        self._move_pointer(self._tail_pointer, self.copy().move_to([0, 0, 0])._nodes[-1], self._nodes[-1]))

    def prepend(self, data) -> Iterable[Animation]:
        return self.add_first(data)

    def add_first(self, data, num_animations: int) -> Iterable[Animation]:
        node = Node(data)
        self._place_node_next_to(node, self._head, LEFT)
        node.set_next(self._head)
        self.add(node)
        FadeOut(node)
        
        # self.add(node._pointer_to_next)
        # FadeOut(node._pointer_to_next)

        def update_sll(mobject, alpha):
            # node._pointer_to_next.fade(1 - alpha)
            node.fade(1 - alpha)

        self._head = node

        self._nodes.insert(0, node)

        AnimationTiming = None
        if num_animations == 1:
            AnimationTiming = AnimationGroup
        elif num_animations == 2:
            AnimationTiming = Succession
        else:
            raise NotImplementedError()

        positioned_node = self.copy().move_to([0, 0, 0])._nodes[0]
        # positioned_node.remove(positioned_node._pointer_to_next)


        return AnimationTiming(AnimationGroup(
            self.animate.move_to([0, 0, 0]),
            UpdateFromAlphaFunc(self, update_sll)
        ),
        self._move_pointer(self._head_pointer, positioned_node, self._nodes[0]))
        # self._move_pointer(self._head_pointer, self._nodes[0], self._nodes[0]))

    # def insert_at_index(self, index: int, data) -> Iterable[Animation]:
    #     trav = Pointer(self._head, 'trav', UP)

    #     animations = []
    #     animations.append(AnimationGroup(*(FadeIn(trav), self.animate.move_to([0, 0, 0]))))
    #     animations.append(self.animate.move_to([0, 0, 0]))

    #     trav_shifts = []
    #     num_to_shift = index - 1
    #     # animations += Succession()
    #     # for i in range(num_to_shift):
    #     animations += [Succession(*[self._move_pointer(trav, 1) for _ in range(num_to_shift)])]
    #         # trav_shifts.append(self._move_pointer(trav, 1))
    #         # trav_shifts.append(AnimationGroup(self._move_pointer(trav, 1)))
    #     # animations += Succession(*trav_shifts)
    #     # animations += trav_shifts


    #     new_node = Node(data)
    #     # new_node.next_to(trav, RIGHT, aligned_edge=trav.get_bottom())

    #     #FIXME: This may get out of bounds
    #     # new_node.next_to(self._nodes[num_to_shift + 1], aligned_edge=self._nodes[num_to_shift + 1].get_bottom())
    #     new_node.move_to(trav.get_bottom())
    #     new_node.move(1)
    #     # self._move_pointer(new_node, 1)
    #     animations.append(AnimationGroup(FadeIn(new_node)))

    #     new_node.set_next(self._nodes[index])
    #     animations.append(AnimationGroup(FadeIn(new_node._pointer_to_next)))

    #     trav_node = self._nodes[num_to_shift]
    #     # animations.append(AnimationGroup(trav_node._pointer_to_next.animate.put_start_and_end_on(start=trav_node._pointer_to_next.get_left(), end=new_node.get_left())))

    #     trav_node._pointer_to_next.generate_target()
    #     trav_node._pointer_to_next.target = SinglyDirectedEdge(start=trav_node._pointer_to_next.get_left(), end=new_node.get_left())
    #     animations.append(AnimationGroup(MoveToTarget(trav_node._pointer_to_next)))

    #     self._nodes.insert(index, new_node)
    #     animations.append(AnimationGroup(*self._flatten()))

    #     # animations.append(AnimationGroup(MoveToTarget(self)))



    #     # Reset trav back to head so the trav shift animations proceed as expected
    #     self._move_pointer(trav, -num_to_shift)
    #     return animations

    def remove_last(self, num_animations: int):
        tail_temp = self._tail

        def update_sll(mobject, alpha):
            self._nodes[-1]._pointer_to_next.fade(alpha)
            tail_temp.fade(alpha)

        self._nodes[-1].remove(self._nodes[-1]._pointer_to_next)
        # self.remove(self._nodes[-1])


        self._nodes.remove(self._nodes[-1])
        self._tail = self._nodes[-1]

        AnimationTiming = None
        if num_animations == 1:
            AnimationTiming = AnimationGroup
        elif num_animations == 2:
            AnimationTiming = Succession
        else:
            raise NotImplementedError()

        return AnimationTiming(AnimationGroup(
            self.animate.move_to([0, 0, 0]),
            UpdateFromAlphaFunc(self, update_sll)
        ),
        self._move_pointer(self._tail_pointer, self._tail.copy(), self._tail))

    def remove_first(self, num_animations: int):
        head_temp = self._head

        def update_sll(mobject, alpha):
            # self._nodes[0]._pointer_to_next.fade(alpha)
            head_temp.fade(alpha)


        self._nodes.remove(self._nodes[0])
        self._head = self._nodes[0]

        AnimationTiming = None
        if num_animations == 1:
            AnimationTiming = AnimationGroup
        elif num_animations == 2:
            AnimationTiming = Succession
        else:
            raise NotImplementedError()

        positioned_node = self.copy().move_to([0, 0, 0])._head
        # positioned_node.remove(positioned_node._pointer_to_next)

        return AnimationTiming(AnimationGroup(
            self.animate.move_to([0, 0, 0]),
            UpdateFromAlphaFunc(self, update_sll)
        ),
        self._move_pointer(self._head_pointer, positioned_node, self._head))

    def remove_at_index(self):
        pass

    def remove(self):
        pass

    

    # FIXME: Hardcoded shift value
    # NOTE: Has the side effect of moving the pointer on the scene without the animation as well
    def _move_pointer(self, pointer: Pointer, positioned_node, actual_node) -> Iterable[Animation]:
        return pointer.move(positioned_node, actual_node)
        # return pointer.move(num_nodes, self._nodes[self._index_of_pointer(pointer) + num_nodes])

    def _index_of_pointer(self, pointer):
        return self._nodes.index(pointer.node)

    # FIXME: Hard coded buff
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