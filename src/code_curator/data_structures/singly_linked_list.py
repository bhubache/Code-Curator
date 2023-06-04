from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Sequence
from typing import Any

from code_curator.animations.singly_linked_list.add_last import AddLast
from code_curator.animations.singly_linked_list.remove_at import RemoveAt
from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.custom_vmobject import CustomVMobject
from manim import Animation
from manim import DOWN
from manim import LEFT
from manim import RIGHT
from manim import UP
from code_curator.null_vmobject import NullVMobject

from .edges.singly_directed_edge import SinglyDirectedEdge
from .nodes.singly_linked_list_node import SLLNode
from .pointers.pointer import Pointer
logger = CustomLogger.getLogger(__name__)

# TODO: Consider using the builder design pattern rather than
#       including for every possible subanimation combination out of the box
# TODO: A lot of duplicate code that needs to be removed.


class SinglyLinkedList(CustomVMobject):
    def __init__(self, *elements: Any, shape: CustomVMobject | None = None) -> None:
        super().__init__()
        self._elements = elements
        self._nodes: list[SLLNode] = []

        if len(self._elements) == 0:
            raise AttributeError('Linked List cannot have zero elements')

        prev = None
        for i in range(0, len(elements)):
            curr = SLLNode(elements[i])
            if i == 0:
                self._head: SLLNode = curr
            if i == len(elements) - 1:
                self._tail: SLLNode = curr
            if i >= 1:
                prev = self._nodes[i - 1]
                self._place_node_next_to(curr, prev, RIGHT)
                prev.set_next(curr)

            self._nodes.append(curr)
            self.add(curr)

        self.head_pointer = Pointer(self._head, self, 'head', DOWN)
        self.tail_pointer = NullVMobject()
        if len(elements) == 1:
            self.tail_pointer = Pointer(self._tail, self, 'tail', UP)
        elif len(elements) > 1:
            self.tail_pointer = Pointer(self._tail, self, 'tail', DOWN)

        self.add(self.head_pointer)
        self.add(self.tail_pointer)

        self.move_to([0, 0, 0])

    def __getitem__(self, index: int) -> SLLNode:
        if index >= len(self):
            raise IndexError(
                f'Index {index} out of bounds for length {len(self)}',
            )
        return self._nodes[index]

    def __setitem__(self, index: int, value: SLLNode) -> None:
        self._nodes[index] = value

    def __delitem__(self, index: int) -> None:
        del self._nodes[index]

    def __iter__(self) -> Iterator[SLLNode]:
        return self._nodes.__iter__()

    def __len__(self) -> int:
        return len(self._nodes)

    @staticmethod
    def create_sll(sll: SinglyLinkedList) -> SinglyLinkedList:
        return SinglyLinkedList(*[node.data for node in sll])

    # def insert(
    #     self,
    #     index: int,
    #     data: Any,
    #     display_first_trav: bool = False,
    #     first_trav_name: str = 'p1',
    #     display_second_trav: bool = False,
    #     second_trav_name: str = 'p2',
    #     trav_position: str = 'start',
    #     aligned: bool = False,
    #     **kwargs,
    # ) -> Insert:
    #     return Insert.create_packager(
    #         sll=self,
    #         index=index,
    #         data=data,
    #         node=self._add_node(index, data, aligned=aligned),
    #         display_first_trav=display_first_trav,
    #         first_trav_name=first_trav_name,
    #         display_second_trav=display_second_trav,
    #         second_trav_name=second_trav_name,
    #         trav_position=trav_position,
    #         aligned=aligned,
    #         sll_calling_method=self.insert,
    #     )

    def add_last(
        self,
        *,
        data: Any,
        display_first_trav: bool = False,
        first_trav_name: str = 'trav',
        trav_position: str = 'start',
        aligned: bool = True,
        **kwargs: Any,
    ) -> AddLast:
        return AddLast.create_packager(
            sll=self,
            index=len(self),
            node=self._add_node(index=len(self), data=data),
            display_first_trav=display_first_trav,
            first_trav_name=first_trav_name,
            trav_position=trav_position,
            aligned=aligned,
            sll_calling_method=self.add_last,
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
        **kwargs: Any,
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
            sll_calling_method=self.remove_at,
        )

    # NOTE: Maybe also remove node from sll?
    # NOTE: Can't remove the node from self._nodes yet
    # TODO: Change node's next attribute!!!!
    def _remove_node(self, index: int) -> SLLNode:
        if index < 0:
            index = len(self) + index

        if index >= len(self):
            raise IndexError(
                f'Index {index} out of bounds for length {len(self)}',
            )

        node = self[index]
        # del self._nodes[index]
        # del self[index]

        if index == 0:
            self._head = self[1]
        if index == len(self) - 1:
            self._tail = self[-2]

        return node

    # TODO: Change node's next attribute!!!!
    # FIXME: Adding node to _nodes BEFORE animating is messing up the forecaster
    def _add_node(self, index: int, data: Any, aligned: bool = True) -> SLLNode:
        if index < 0:
            index = len(self) + index

        if index > len(self):
            raise IndexError(
                f'Index {index} out of bounds for length {len(self)}',
            )

        node = SLLNode(data)
        # self._nodes.insert(index, node)
        if index == 0:
            self._head = node
        if index == len(self):
            self._tail = node

        # TODO: Adjust all of these because the node is not yet inserted!!!
        if self._adding_to_front(index):
            if aligned:
                # node.next_to(
                # self[1].container, LEFT, buff=(self[1].pointer_to_next.length + (2 * self[1].container.radius))
                # )
                # node.next_to(self[1].container, LEFT, buff=0)
                node.align_to(self[1].container, LEFT + DOWN)
                node.shift(
                    LEFT * (
                        (self[0].radius * 2) +
                        self[1].pointer_to_next.length
                    ),
                )
                node.set_next(self[1])
            else:
                raise NotImplementedError(
                    'Nonaligned insertion of a node at the front of linked list is not yet supported',
                )
        elif self._adding_in_between_head_and_tail(index):
            # FIXME: Fix index now node isn't inserted before this logic!!!
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
        elif self._adding_to_back(index):
            if self[0].pointer_to_next is None:
                node.next_to(self[-1], RIGHT, buff=2 * self[0].radius)
            else:
                node.next_to(
                    self[-1], RIGHT,
                    buff=self[0].pointer_to_next.length,
                )
            self[-1].set_next(node)
            self[-1].pointer_to_next.set_opacity(0)

            if not aligned:
                node.shift(DOWN)
                self[-1].pointer_to_next.become(
                    SinglyDirectedEdge(
                        start=self[-1].pointer_to_next.start, end=node.get_container_left(),
                    ),
                )
        else:
            raise Exception(
                f'Attempting to add node at index {index} for length {len(self)}',
            )

        self._nodes.insert(index, node)

        if node.pointer_to_next is not None:
            node.add(node.pointer_to_next)
        node.add(node.container)
        self.add(node)

        return node

    def _adding_to_front(self, index: int) -> bool:
        return index == 0

    def _adding_in_between_head_and_tail(self, index: int) -> bool:
        return 0 < index < len(self)

    def _adding_to_back(self, index: int) -> bool:
        return index == len(self)

    # FIXME: Hardcoded shift value
    # NOTE: Has the side effect of moving the pointer on the scene without the animation as well
    def _move_pointer(self, pointer: Pointer, positioned_node: SLLNode, actual_node: SLLNode) -> Iterable[Animation]:
        return pointer.move(positioned_node, actual_node)
        # return pointer.move(num_nodes, self._nodes[self._index_of_pointer(pointer) + num_nodes])

    def _immediately_move_pointer(self, pointer: Pointer, positioned_node: SLLNode, actual_node: SLLNode) -> None:
        pointer.immediately_move(positioned_node, actual_node)

    def _index_of_pointer(self, pointer: Pointer) -> int:
        return self._nodes.index(pointer.node)

    # FIXME: Hard coded buff
    def _place_node_next_to(
        self,
        node: SLLNode,
        other: SLLNode,
        direction: Sequence[int] = RIGHT,
        buff: float = 1,
    ) -> None:
        node.next_to(other, direction, buff=buff)
