from __future__ import annotations
import math

from typing import Iterable, Any

from ..nodes.singly_linked_list_node import SLLNode
from ..pointers.pointer import Pointer
from ..edges.singly_directed_edge import SinglyDirectedEdge
from animations.singly_linked_list.subanimations.fade_in_node import FadeInNode
from animations.singly_linked_list.subanimations.fade_in_pointer import FadeInPointer
from animations.singly_linked_list.subanimations.grow_pointer import GrowPointer
from animations.singly_linked_list.subanimations.move_trav import MoveTrav
from animations.singly_linked_list.subanimations.center_sll import CenterSLL
from animations.singly_linked_list.add_first import AddFirst
from animations.singly_linked_list.add_last import AddLast
from animations.singly_linked_list.remove_first import RemoveFirst
from animations.singly_linked_list.remove_last import RemoveLast
from animations.singly_linked_list.insert import Insert
from animations.singly_linked_list.remove_at import RemoveAt
from manim import VMobject, DOWN, LEFT, UP, RIGHT, FadeIn, FadeOut, Animation, AnimationGroup, Succession, UpdateFromAlphaFunc, VGroup

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

# The following imports are for development
from animations.singly_linked_list.subanimations.fade_in_pointer import FadeInPointer
from animations.singly_linked_list.subanimations.fade_in_node import FadeInNode
from animations.animation_package import AnimationPackage
from animations.package_animation import PackageAnimation
import sys

# TODO:
# If animations are successive, use the successive animations
# If the animations are used synchronously, determine if they're orthogonal
#   1. If they're orthogonal, use them as is
#   2. If they're not orthogonal, use the successive animation tactic to find their ending mobject
#
# How am I going to determine if animations are orthogonal??
# Animations are orthogonal if the objects involved are not the same or one isn't
# a superset of the other OR if different animations are being applied.
# Shifting a sub linked list and center the sll are NOT orthogonal because we are applying the SAME
# kind of animation (movement) on two objects that are either the same, or one is a subset of the other.
# Create an n x n grid to note the animations that are dependent on each other (every animation is dependent on itself).
# NOTE: Be mindful of the order of some animation combinations!!!
# NOTE: When checking for dependency in the table, check both orderings of subanimations because the table doesn't display
#       the symmetry


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
        self._animation_package = AnimationPackage(self)

        self._add_first = AddFirst(self)
        self._insert = Insert(self)
        self._add_last = AddLast(self)
        self._remove_first = RemoveFirst(self)
        self._remove_last = RemoveLast(self)
        self._remove_at = RemoveAt(self)

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
        # if index < 0:
        #     raise IndexError(f'Index {index} is out of bounds for length {len(self)}')
        return self._nodes[index]
    
    def __setitem__(self, index: int, value: SLLNode) -> None:
        self._nodes[index] = value

    def __iter__(self):
        return self._nodes.__iter__()
    
    def __len__(self):
        return len(self._nodes)
    
    # def save_state(self, unique_id: str = None) -> SinglyLinkedList:
    #     if unique_id is None:
    #         return super().save_state()
        
    #     if unique_id in self._saved_states:
    #         # Prevent exponential growth of data
    #         # See manim docs for mobject
    #         self._saved_states[unique_id] = None
    #     self._saved_states[unique_id] = self.copy()
    #     return self
    
    # def restore(self, unique_id: str = None) -> SinglyLinkedList:
    #     if unique_id is None:
    #         saved_state = super().restore()
    #         return saved_state
    #         # return super().restore()
        
    #     if unique_id not in self._saved_states or self._saved_states[unique_id] is None:
    #         raise Exception(f'Trying to restore state {unique_id} without having saved')
        
    #     saved_state = self._saved_states[unique_id]
    #     self.become(saved_state)
        
    #     # self.become(self._saved_states[unique_id])
    #     return self
        
    
    @staticmethod
    def create_sll(sll: SinglyLinkedList) -> SinglyLinkedList:
        return SinglyLinkedList(*[node.data._value for node in sll])

    # def ensure_submobjects_added(func):
    #     '''Ensures all nodes in linked list are added to the VMobject.

    #     A node may be visible on the screen, but that doesn't guarantee
    #     it is in the submobjects member variable of the mobject. When a
    #     node is made visible on the screen but not added to the mobjects'
    #     submobjects list, subsequent animations using that node will not
    #     be able to animate it. Here, any nodes found in self._nodes that
    #     aren't in submobjects are added.
    #     '''
    #     def inner(obj, *args, **kwargs):
    #         for sub in obj._nodes:
    #             if sub not in obj.submobjects:
    #                 logger.info(f'NOT IN: {sub}')
    #             obj.add(sub)

    #         return func(obj, *args, **kwargs)
        
    #     return inner

    # def ensure_test(func):
    #     def inner(obj, *args, **kwargs):
    #         for sub in obj._nodes:
    #             if sub not in obj.submobjects:
    #                 logger.info(f'TEST SUB NOT IN: {sub}')
    #                 obj.add(sub)

    #             for component in sub.get_visible_components():
    #                 if component not in sub.submobjects:
    #                     logger.info(f'TEST COMPONENT NOT IN: {component}')
    #                     sub.add(component)

    #         return func(obj, *args, **kwargs)
        
    #     return inner
    
    #######################################################################
    # The following animations add a node to the front of the linked list #
    #######################################################################
    def add_first_all_together(self, data: Any, pointer_animation_type: str = 'grow') -> PackageAnimation:
        return self._add_first.all_together(self._add_node(0, data), pointer_animation_type)
    
    def add_first_node_then_rest(self, data: Any, pointer_animation_type: str = 'grow') -> PackageAnimation:
        return self._add_first.node_then_rest(self._add_node(0, data), pointer_animation_type)
    
    def add_first_node_and_pointer_then_rest(self, data: Any, pointer_animation_type: str = 'grow') -> PackageAnimation:
        return self._add_first.node_and_pointer_then_rest(self._add_node(0, data), pointer_animation_type)
    
    def add_first_node_and_pointer_and_trav_then_rest(self, data: Any, pointer_animation_type: str = 'grow') -> PackageAnimation:
        return self._add_first.node_and_pointer_and_trav_then_rest(self._add_node(0, data), pointer_animation_type)
    
    def add_first_node_and_trav_then_rest(self, data: Any, pointer_animation_type: str = 'grow') -> PackageAnimation:
        return self._add_first.node_and_trav_then_rest(self._add_node(0, data), pointer_animation_type)
    
    def add_first_node_and_center_then_rest(self, data: Any, pointer_animation_type: str = 'grow') -> PackageAnimation:
        return self._add_first.node_and_center_then_rest(self._add_node(0, data), pointer_animation_type)
    
    def add_first_node_then_pointer_then_rest(self, data: Any, pointer_animation_type: str = 'grow') -> PackageAnimation:
        return self._add_first.node_then_pointer_then_rest(self._add_node(0, data), pointer_animation_type)
    
    def add_first_node_then_trav_then_rest(self, data: Any, pointer_animation_type: str = 'grow') -> PackageAnimation:
        return self._add_first.node_then_trav_then_rest(self._add_node(0, data), pointer_animation_type)
    
    def add_first_node_then_center_then_rest(self, data: Any, pointer_animation_type: str = 'grow') -> PackageAnimation:
        return self._add_first.node_then_center_then_rest(self._add_node(0, data), pointer_animation_type)
    
    def add_first_node_then_pointer_then_trav_then_center(self, data: Any, pointer_animation_type: str = 'grow') -> PackageAnimation:
        return self._add_first.node_then_pointer_then_trav_then_center(self._add_node(0, data), pointer_animation_type)
    
    def add_first_node_then_center_then_pointer_then_trav(self, data: Any, pointer_animation_type: str = 'grow') -> PackageAnimation:
        return self._add_first.node_then_center_then_pointer_then_trav(self._add_node(0, data), pointer_animation_type)
    
    def add_first_node_then_center_then_trav_then_pointer(self, data: Any, pointer_animation_type: str = 'grow') -> PackageAnimation:
        return self._add_first.node_then_center_then_trav_then_pointer(self._add_node(0, data), pointer_animation_type)
    
    def add_first_center_then_node_then_pointer_then_trav(self, data: Any, pointer_animation_type: str = 'grow') -> PackageAnimation:
        return self._add_first.center_then_node_then_pointer_then_trav(self._add_node(0, data), pointer_animation_type)
    
    def add_first_center_then_node_then_trav_then_pointer(self, data: Any, pointer_animation_type: str = 'grow') -> PackageAnimation:
        return self._add_first.center_then_node_then_trav_then_pointer(self._add_node(0, data), pointer_animation_type)
    
    #############################################################
    # The following animations insert a node in the linked list #
    #############################################################
    def insert_test(self, index: int, data: Any, pointer_animation_type: str = 'fade', display_trav: bool = False, trav_name: str = 'trav', trav_position: str = 'start') -> PackageAnimation:
        return Insert(self).insert_test(
            index,
            self._add_node(index, data),
            pointer_animation_type=pointer_animation_type,
            display_trav=display_trav,
            trav_name=trav_name,
            trav_position=trav_position
        )
    
    # TODO: Figure out using the same instantiation of Insert makes this incredibly slow!!!
    def insert_all_together(self, index: int, data: Any, pointer_animation_type: str = 'fade'):
        logger.info(id(self))
        insert_obj = Insert(self)
        return insert_obj.all_together(
            index,
            self._add_node(index, data),
            pointer_animation_type=pointer_animation_type,
            aligned=True
        )

    
    def _add_node(self, index: int, data: Any) -> None:
        node = SLLNode(data)
        if index == 0:
            node.next_to(self[index], LEFT, buff=1)
        # elif index < len(self):
        #     node.move_to(self[index].container)
        if index > len(self):
            raise NotImplementedError('Adding to the end of a SLL is not supported.')
        node.set_next(self[index])

        node.add(node._pointer_to_next)
        node.add(node._container)

        if index == 0:
            self._head = node
        if index == len(self):
            self._tail = node

        self._nodes.insert(index, node)
        self.add(node)

        return node

    # @ensure_submobjects_added
    # def insert(self, index: int, data: Any):
    #     return self._insert.one_by_one(
    #         index=index,
    #         data=data,
    #         aligned=False,
    #         trav_displayed=False,
    #         prev_node_pointer_is_first=False,
    #         trav_position='start'
    #     )

    # @ensure_submobjects_added
    # def remove_last(self):
    #     return self._remove_last.all_together()

    # @ensure_submobjects_added
    # def remove_first(self):
    #     return self._remove_first.all_together()

    # @ensure_submobjects_added
    # def remove_at(self, index: int, end_index: int = None):
    #     # End index is exclusive
    #     if end_index is None:
    #         end_index = index + 1
    #     return self._remove_at.one_by_one(
    #         index=index,
    #         end_index=end_index,
    #         trav_position='start',
    #         trav_names=['p1', 'p2'],
    #         pointer_movement='specific'
    #     )

        
    # @ensure_submobjects_added
    # # @ensure_test
    # def move_to_origin(self):
    #     logger.info(self.submobjects)
    #     logger.info(len(self.submobjects))
    #     sll = VGroup(*self.submobjects)
    #     logger.info(f'sll center: {sll.get_center()}')
    #     logger.info(f'self center: {self.get_center()}')
    #     return VGroup(*self.submobjects).animate.move_to([0, 0, 0])
    #     # return self.animate.move_to([0, 0, 0])

    

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

    # def _flatten(self):
    #     data_list = [node._data for node in self._nodes]
    #     flattened_copy = create_sll(data_list)
        
    #     animations = []
    #     for self_node, flattened_node in zip(self._nodes, flattened_copy._nodes):
    #         animations.append(self_node.animate.move_to(flattened_node))
    #     # animations.append(self.move_to_origin())
    #     return animations

    # def fade_out_node(self, node: SLLNode) -> None:
    #     FadeOut(node)

    # def fade_in_node(self, node: SLLNode) -> None:
    #     FadeIn(node)

    # def animate_fade_out_node(self, node: SLLNode) -> Animation:
    #     return FadeOut(node)

    # def animate_fade_in_node(self, node: SLLNode) -> Animation:
    #     return FadeIn(node)