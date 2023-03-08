import math

from typing import Iterable, Any

from ..nodes.singly_linked_list_node import SLLNode
from ..pointers.pointer import Pointer
from ..edges.singly_directed_edge import SinglyDirectedEdge
from animations.singly_linked_list.add_first import AddFirst
from animations.singly_linked_list.add_last import AddLast
from animations.singly_linked_list.remove_first import RemoveFirst
from animations.singly_linked_list.remove_last import RemoveLast
from animations.singly_linked_list.insert import Insert
from animations.singly_linked_list.remove_at import RemoveAt
from manim import VMobject, DOWN, LEFT, UP, RIGHT, FadeIn, FadeOut, Animation, AnimationGroup, Succession, UpdateFromAlphaFunc, VGroup

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

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
        if index < 0:
            raise IndexError(f'Index {index} is out of bounds for length {len(self)}')
        return self._nodes[index]
    
    def __setitem__(self, index: int, value: SLLNode) -> None:
        self._nodes[index] = value

    def __iter__(self):
        return self._nodes.__iter__()
    
    def __len__(self):
        return len(self._nodes)

    def ensure_submobjects_added(func):
        '''Ensures all nodes in linked list are added to the VMobject.

        A node may be visible on the screen, but that doesn't guarantee
        it is in the submobjects member variable of the mobject. When a
        node is made visible on the screen but not added to the mobjects'
        submobjects list, subsequent animations using that node will not
        be able to animate it. Here, any nodes found in self._nodes that
        aren't in submobjects are added.
        '''
        def inner(obj, *args, **kwargs):
            for sub in obj._nodes:
                if sub not in obj.submobjects:
                    logger.info(f'NOT IN: {sub}')
                obj.add(sub)

            return func(obj, *args, **kwargs)
        
        return inner

    def ensure_test(func):
        def inner(obj, *args, **kwargs):
            for sub in obj._nodes:
                if sub not in obj.submobjects:
                    logger.info(f'TEST SUB NOT IN: {sub}')
                    obj.add(sub)

                for component in sub.get_visible_components():
                    if component not in sub.submobjects:
                        logger.info(f'TEST COMPONENT NOT IN: {component}')
                        sub.add(component)

            return func(obj, *args, **kwargs)
        
        return inner

    @ensure_submobjects_added
    def append(self, data: Any, num_animations: int):
        '''Delegates to add_last.'''
        return self.add_last(data)


    # TODO: Clean up!
    @ensure_submobjects_added
    def add_last(self, data: Any):
        '''Adds a node to the end of the linked list.

        Note any side effects or similar things here.

        Args:
            data: Value to be stored in the new node.
            num_animations: The number of sequential animations to be played.

        Returns:
            An animation grouping that will play the animations according
            to the number of animations specified by num_animations.
            
            For instance:
                If 1 animation is specified, then the animations
                will be returned within an AnimationGroup.

                If 2 animations is specified, then the animations
                will be returned within a Succession.
        '''
        return self._add_last.node_then_pointer_then_trav_then_center(data)

    @ensure_submobjects_added
    def prepend(self, data: Any, num_animations: int):
        '''Delegates to add_first.'''
        return self.add_first(data)

    @ensure_submobjects_added
    def add_first(self, data):
        '''Add a new node to the front of the linked list.

        Note any side effects or similar things here.

        Args:
            data: Value to be stored in the new node.
            num_animations: The number of sequential animations to be played.

        Returns:
            An animation grouping that will play the animations according
            to the number of animations specified by num_animations.
            
            For instance:
                If 1 animation is specified, then the animations
                will be returned within an AnimationGroup.

                If 2 animations is specified, then the animations
                will be returned within a Succession.
        '''
        return self._add_first.node_then_everything_else(data)

    @ensure_submobjects_added
    def insert(self, index: int, data: Any):
        return self._insert.one_by_one(
            index=index,
            data=data,
            aligned=False,
            trav_displayed=False,
            prev_node_pointer_is_first=False,
            trav_position='start'
        )

    @ensure_submobjects_added
    def remove_last(self):
        '''Removes the last node from the linked list.

        Note any side effects or similar things here.

        Args:
            num_animations: The number of sequential animations to be played.

        Returns:
            An animation grouping that will play the animations according
            to the number of animations specified by num_animations.
            
            For instance:
                If 1 animation is specified, then the animations
                will be returned within an AnimationGroup.

                If 2 animations is specified, then the animations
                will be returned within a Succession.
        '''
        return self._remove_last.all_together()

    @ensure_submobjects_added
    def remove_first(self):
        '''Removes the first node from the linked list.

        Note any side effects or similar things here.

        Args:
            num_animations: The number of sequential animations to be played.

        Returns:
            An animation grouping that will play the animations according
            to the number of animations specified by num_animations.
            
            For instance:
                If 1 animation is specified, then the animations
                will be returned within an AnimationGroup.

                If 2 animations is specified, then the animations
                will be returned within a Succession.
        '''
        return self._remove_first.all_together()

    @ensure_submobjects_added
    def remove_at(self, index: int, end_index: int = None):
        # End index is exclusive
        if end_index is None:
            end_index = index + 1
        return self._remove_at.one_by_one(
            index=index,
            end_index=end_index,
            trav_position='start',
            trav_names=['p1', 'p2'],
            pointer_movement='specific'
        )

        
    # @ensure_submobjects_added
    # @ensure_test
    def move_to_origin(self):
        logger.info(self.submobjects)
        logger.info(len(self.submobjects))
        sll = VGroup(*self.submobjects)
        logger.info(f'sll center: {sll.get_center()}')
        logger.info(f'self center: {self.get_center()}')
        return VGroup(*self.submobjects).animate.move_to([0, 0, 0])
        # return self.animate.move_to([0, 0, 0])

    

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

    def _flatten(self):
        data_list = [node._data for node in self._nodes]
        flattened_copy = create_sll(data_list)
        
        animations = []
        for self_node, flattened_node in zip(self._nodes, flattened_copy._nodes):
            animations.append(self_node.animate.move_to(flattened_node))
        # animations.append(self.move_to_origin())
        return animations

    def fade_out_node(self, node: SLLNode) -> None:
        FadeOut(node)

    def fade_in_node(self, node: SLLNode) -> None:
        FadeIn(node)

    def animate_fade_out_node(self, node: SLLNode) -> Animation:
        return FadeOut(node)

    def animate_fade_in_node(self, node: SLLNode) -> Animation:
        return FadeIn(node)