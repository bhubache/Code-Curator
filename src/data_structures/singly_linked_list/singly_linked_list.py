import math
import inspect

from manim import VMobject, DOWN, LEFT, UP, RIGHT, FadeIn, FadeOut, Animation, AnimationGroup, Succession, UpdateFromAlphaFunc, Circle, Create, Transform, ReplacementTransform, TransformMatchingShapes, VGroup, ArcBetweenPoints, Wait

from ..nodes.singly_linked_list_node import SLLNode as Node
from ..pointers.pointer import Pointer
from ..edges.singly_directed_edge import SinglyDirectedEdge

from typing import Iterable, Any


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

        if len(elements) == 0:
            raise AttributeError('Linked List cannot have zero elements')

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
                    logger.info('NOT IN')
                obj.add(sub)

            return func(obj, *args, **kwargs)
        
        return inner

    @ensure_submobjects_added
    def append(self, data: Any, num_animations: int):
        '''Delegates to add_last.'''
        return self.add_last(data)


    # TODO: Clean up!
    @ensure_submobjects_added
    def add_last(self, data: Any, num_animations: int):
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
        node = Node(data)
        self._place_node_next_to(node, self._tail)
        self._tail.set_next(node)
        self.add(node)
        FadeOut(node)

        self._nodes.append(node)
        self._tail = node

        def update_sll(mobject, alpha):
            self._nodes[len(self._nodes) - 2]._pointer_to_next.fade(1 - alpha)
            node.fade(1 - alpha)

        AnimationTiming = None
        if num_animations == 1:
            AnimationTiming = AnimationGroup
        elif num_animations == 2:
            AnimationTiming = Succession
        else:
            raise NotImplementedError()

        positioned_node = self.copy().move_to([0, 0, 0])._nodes[-1]

        return AnimationTiming(AnimationGroup(
            self._move_to_origin(),
            UpdateFromAlphaFunc(self, update_sll)
        ),
        self._move_pointer(self._tail_pointer, positioned_node, self._nodes[-1]))

    @ensure_submobjects_added
    def prepend(self, data: Any, num_animations: int):
        '''Delegates to add_first.'''
        return self.add_first(data)

    @ensure_submobjects_added
    def add_first(self, data, num_animations: int):
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
        node = Node(data)
        self._place_node_next_to(node, self._head, LEFT)
        node.set_next(self._head)
        self.add(node)
        FadeOut(node)

        def update_sll(mobject, alpha):
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


        return AnimationTiming(AnimationGroup(
            self._move_to_origin(),
            UpdateFromAlphaFunc(self, update_sll)
        ),
        self._move_pointer(self._head_pointer, positioned_node, self._nodes[0]))

    @ensure_submobjects_added
    def insert(self, index: int, data: Any):
        if index < 0 or index >= len(self._nodes):
            raise IndexError(f'Index {index} is out of bounds for bounds [0, {len(self._nodes)})')

        if index == 0: return self.add_first(data)
        if index == len(self._nodes) - 1: return self.add_last(data)

        trav = Pointer(self._head, 'trav', direction=self._head_pointer.opposite_of_direction())

        move_trav_animations = []
        for i, node in enumerate(self._nodes):
            move_trav_animations.append(
                self._move_pointer(trav, node, node)
            )

            if i == index - 1:
                break

        prev_node = self._nodes[index - 1]
        new_node = Node(data)
        # FIXME: Hardcoded relative positioning DOWN
        new_node.next_to(self._nodes[index]._container, DOWN)
        new_node.set_next(self._nodes[index])

        prev_node.next = new_node
        # FIXME: Hardcoded moving prev pointer to left of new_node container
        pointer_to_next_start, _ = prev_node._pointer_to_next.get_start_and_end()
        # TODO: Fix arrow head changing size!!
        # FIXME: Hardcoded new_node container left end position for previous pointer
        # change_prev_pointer = prev_node._pointer_to_next.animate.put_start_and_end_on(pointer_to_next_start, new_node.get_container_left())

        moved_prev_pointer = SinglyDirectedEdge(start=pointer_to_next_start, end=new_node.get_container_left())

        # TODO: Make sure the 'becomed' arrow is able to be manipulated properly
        change_prev_pointer = prev_node._pointer_to_next.animate.become(moved_prev_pointer)

        sub_list_to_move = VGroup(*[node for i, node in enumerate(self._nodes) if i >= index])

        # new_node_pointer_start, new_node_pointer_end = new_node._pointer_to_next.get_start_and_end()
        sub_list_to_move.save_state()
        new_node.save_state()
        self.save_state()
        trav.save_state()
        self._tail_pointer.save_state()

        self._nodes.insert(index, new_node)

        self_copy = SinglyLinkedList(*[node.data._value for node in self._nodes])
        shift_left_value = self.get_left()[0] - self_copy.get_left()[0]

        distance_to_shift = abs(self._nodes[0].get_left() - self._nodes[1].get_left())
        distance_up = abs(new_node.get_container_top() - self._nodes[0].get_container_top())
        def flatten_list(self, alpha):
            self.restore()
            self.shift(LEFT * shift_left_value * alpha)

            new_node.restore()
            new_node.shift(LEFT * shift_left_value * alpha)
            new_node.shift(UP * distance_up * alpha)

            sub_list_to_move.restore()
            sub_list_to_move.shift(LEFT * shift_left_value * alpha)
            sub_list_to_move.shift(RIGHT * distance_to_shift * alpha)

            self._nodes[index - 1]._pointer_to_next.become(SinglyDirectedEdge(start=self._nodes[index - 1].get_container_right(), end=self._nodes[index].get_container_left()))

            trav.restore()
            for i, node in enumerate(self._nodes):
                self._immediately_move_pointer(trav, node, node)

                if i == index - 1:
                    break

            self._tail_pointer.restore()
            self._tail_pointer.shift(RIGHT * shift_left_value * alpha)
            def rotate_start():
                start, _ = new_node._pointer_to_next.get_start_and_end()
                curr_x = start[0]
                curr_y = start[1]

                origin_x, origin_y, _ = new_node.get_container_center()
                angle = -(math.pi / 2 * alpha)
                sine = math.sin(angle)
                cosine = math.cos(angle)

                new_x = origin_x + cosine * (curr_x - origin_x) - sine * (curr_y - origin_y)
                new_y = origin_y - sine * (curr_x - origin_x) + cosine * (curr_y - origin_y)
                return [new_x, new_y, 0]

            def rotate_end():
                # FIXME: Hardcoded bottom of container
                curr_x, curr_y, _ = self._nodes[index + 1].get_container_bottom()

                angle = -(math.pi / 2 * alpha)
                sine = math.sin(angle)
                cosine = math.cos(angle)

                origin_x, origin_y, _ = self._nodes[index + 1].get_container_center()
                curr_x = curr_x - origin_x
                curr_y = curr_y - origin_y

                new_x = curr_x * cosine - curr_y * sine
                new_y = curr_x * sine + curr_y * cosine

                new_x += origin_x
                new_y += origin_y
                return [new_x, new_y, 0]

            # Move next pointer on node being inserted
            # new_node_start, new_node_end = new_node._pointer_to_next.get_start_and_end()
            new_node._pointer_to_next.become(
                SinglyDirectedEdge(
                    start=rotate_start(),
                    end=rotate_end()
                )
            )

        return Succession(
            FadeIn(trav),
            *move_trav_animations,
            FadeIn(new_node),
            change_prev_pointer,
            AnimationGroup(
                UpdateFromAlphaFunc(self, flatten_list),
                FadeOut(trav)
            )
        )

    @ensure_submobjects_added
    def remove_last(self, num_animations: int):
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
        tail_temp = self._tail

        self_copy = self.copy()
        self_copy.remove(self_copy._nodes[-1])
        self_copy._nodes[-2].remove(self_copy._nodes[-2]._pointer_to_next)
        self_copy.remove(self_copy._tail_pointer)
        self_copy.move_to([0, 0, 0])
        shift_left_value = self.get_left()[0] - self_copy.get_left()[0]

        def update_sll(mobject, alpha):
            self._nodes[-1]._pointer_to_next.fade(alpha)
            tail_temp.fade(alpha)

            if alpha == 1:
                self._nodes[-1].remove(self._nodes[-1]._pointer_to_next)
                self.remove(tail_temp)


        del self._nodes[-1]
        self._tail = self._nodes[-1]

        AnimationTiming = None
        if num_animations == 1:
            AnimationTiming = AnimationGroup
        elif num_animations == 2:
            AnimationTiming = Succession
        else:
            raise NotImplementedError()

        return AnimationTiming(AnimationGroup(
            self.animate.shift(LEFT * shift_left_value),
            UpdateFromAlphaFunc(self, update_sll)
        ),
        self._move_pointer(self._tail_pointer, self_copy._nodes[-2], self._tail))

    @ensure_submobjects_added
    def remove_first(self, num_animations: int):
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
        head_temp = self._head

        self_copy = self.copy()
        self_copy.remove(self_copy._nodes[0])
        self_copy._nodes[0].remove(self_copy._nodes[0]._pointer_to_next)
        self_copy.remove(self_copy._head_pointer)
        self_copy.move_to([0, 0, 0])
        shift_left_value = self.get_right()[0] - self_copy.get_right()[0]
        logger.info(shift_left_value)

        def update_sll(mobject, alpha):
            # self._nodes[0]._pointer_to_next.fade(alpha)
            head_temp.fade(alpha)

            if alpha == 1:
                head_temp.remove(head_temp._pointer_to_next)
                self.remove(head_temp)


        # self._nodes.remove(self._nodes[0])
        del self._nodes[0]
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
            # self._move_to_origin(),
            self.animate.shift(LEFT * shift_left_value),
            UpdateFromAlphaFunc(self, update_sll)
        ),
        self._move_pointer(self._head_pointer, self_copy._nodes[1], self._head))

    @ensure_submobjects_added
    def remove_at_index(self, index: int):
        if index < 0 or index >= len(self._nodes):
            raise IndexError(f'Index {index} is out of bounds for bounds [0, {len(self._nodes)})')

        if index == 0: return self.remove_first()
        if index == len(self._nodes) - 1: return self.remove_last()

        original_prev_removed_node_next_pointer_copy = self._nodes[index - 1]._pointer_to_next.copy()

        p1 = Pointer(self._head, 'p1', direction=self._head_pointer.opposite_of_direction())
        p2 = Pointer(self._nodes[1], 'p2', direction=self._head_pointer.opposite_of_direction())

        move_trav_animations = []
        for i, node in enumerate(self._nodes):
            if i > index: break

            next_node = self._nodes[i + 1]
            if i < index:
                move_trav_animations.append(
                    AnimationGroup(
                        self._move_pointer(p1, node, node),
                        self._move_pointer(p2, next_node, next_node)
                    )
                )
            elif i == index:
                move_trav_animations.append(
                    self._move_pointer(p2, next_node, next_node)
                )

        shrunken_next_pointer = SinglyDirectedEdge(
            start=p1.node._pointer_to_next.get_start_and_end()[0],
            end=p1.node._pointer_to_next.get_start_and_end()[0] + [p1.node._pointer_to_next.tip.length, 0, 0]
        )
        extended_next_pointer = SinglyDirectedEdge(
            start=p1.node._pointer_to_next.get_start_and_end()[0],
            end=p1.node.next.get_container_left()
        )
        curved_next_pointer = SinglyDirectedEdge.create_curved_pointer(
            start=p1.node._pointer_to_next.get_start_and_end()[0],
            end=p2.node.get_container_left()
        )

        p1.node._pointer_to_next.save_state()

        def normal_to_shrunken(mobject, alpha):
            p1.node._pointer_to_next.restore()
            diff_width = (
                (p1.node._pointer_to_next.get_start_and_end()[1] - p1.node._pointer_to_next.get_start_and_end()[0])[0] * 1 - alpha
            )

            p1.node._pointer_to_next.become(
                SinglyDirectedEdge(
                    start=p1.node._pointer_to_next.get_start_and_end()[0],
                    end=(p1.node._pointer_to_next.get_start_and_end()[0] + [p1.node._pointer_to_next.tip.length * (alpha), 0, 0]) + [diff_width, 0, 0]
                )
            )

            if alpha == 1:
                p1.node._pointer_to_next.save_state()

        def shrunken_to_normal(mobject, alpha):
            p1.node._pointer_to_next.restore()
            p1.node._pointer_to_next.become(
                SinglyDirectedEdge(
                    start=p1.node._pointer_to_next.get_start_and_end()[0],
                    end=(
                        p1.node._pointer_to_next.get_start_and_end()[1]
                        + (
                            (p1.node.next.get_container_left() - p1.node._pointer_to_next.get_start_and_end()[0]) * [alpha, 0, 0]
                        )
                        - [(p1.node._pointer_to_next.tip.length * alpha), 0, 0]
                    )
                )
            )

            if alpha == 1:
                p1.node._pointer_to_next.save_state()

        def normal_to_curved(mobject, alpha):
            p1.node._pointer_to_next.restore()
            start = p1.node._pointer_to_next.get_start_and_end()[0]
            end = p1.node._pointer_to_next.get_start_and_end()[1] + ((p2.node.get_container_left() - p1.node._pointer_to_next.get_start_and_end()[1]) * [alpha, 0, 0])
            p1.node._pointer_to_next.become(
                SinglyDirectedEdge.create_curved_pointer(
                    start=start,
                    end=end,
                    angle=alpha * (1.25 + p1.node.radius)
                )
            )

        node_to_remove = self._nodes[index]
        del self._nodes[index]

        def fade_out_removed_node(mobject, alpha):
            node_to_remove.fade(alpha)

            if alpha == 1:
                self.remove(node_to_remove)

        self.save_state()

        self_copy = SinglyLinkedList(*[node.data._value for node in self._nodes])
        shift_left_value = self.get_left()[0] - self_copy.get_left()[0]
        # shift_left_value = self._nodes[0].get_left() - self._nodes[0].get_right()

        curved_end = p1.node._pointer_to_next.get_start_and_end()[1]
        sub_list_to_flatten = VGroup(*self._nodes[index:], self._tail_pointer)
        sub_list_to_flatten.save_state()
        self.prev_alpha = 0
        def flatten_list(mobject, alpha):
            # self.restore()
            d_alpha = alpha - self.prev_alpha
            self.prev_alpha = alpha
            self.shift(LEFT * shift_left_value * d_alpha)

            final_start = original_prev_removed_node_next_pointer_copy.get_start_and_end()[0]
            final_end = original_prev_removed_node_next_pointer_copy.get_start_and_end()[1] + (LEFT * shift_left_value * alpha)

            sub_list_to_flatten.restore()
            sub_list_to_flatten.shift(LEFT * abs(final_end - p2.node.get_container_left()) * alpha)

            curr_end = p1.node._pointer_to_next.get_start_and_end()[1]
            p1.node._pointer_to_next.become(
                SinglyDirectedEdge.create_curved_pointer(
                    start=final_start + (LEFT * shift_left_value * alpha),
                    end=sub_list_to_flatten[0].get_container_left(),
                    angle=(1 - alpha) * (1.25 + p1.node.radius)
                )
            )

            if alpha == 1:
                p1.node._pointer_to_next.become(
                    SinglyDirectedEdge(
                        start=final_start + (LEFT * shift_left_value * alpha),
                        end=final_end
                    )
                )

            p1.fade(alpha)
            p2.fade(alpha)


        return Succession(
            AnimationGroup(
                FadeIn(p1),
                FadeIn(p2)
            ),
            *move_trav_animations,
            UpdateFromAlphaFunc(self, normal_to_shrunken),
            UpdateFromAlphaFunc(self, shrunken_to_normal),
            UpdateFromAlphaFunc(self, normal_to_curved),
            # ReplacementTransform(
            #     p1.node._pointer_to_next,
            #     SinglyDirectedEdge.create_curved_pointer(
            #         start=p1.node._pointer_to_next.get_start_and_end()[0],
            #         end=p2.node.get_container_left()
            #     )
            # ),
            UpdateFromAlphaFunc(self, fade_out_removed_node),
            UpdateFromAlphaFunc(self, flatten_list)
            # ReplacementTransform(
            #     p1.node._pointer_to_next,
            #     SinglyDirectedEdge(
            #         start=original_prev_removed_node_next_pointer_copy.get_start_and_end()[0],
            #         end=original_prev_removed_node_next_pointer_copy.get_start_and_end()[1]
            #     )
            # )
        )

        

    def _move_to_origin(self):
        # for _ in dir(self.submobjects[0]):
        #     print(_)
        for sub in self.submobjects:
            # logger.info(sub)
            if isinstance(sub, Node) and not sub.is_visible:
                logger.info(sub)
                # self.remove(sub)
        return self.animate.move_to([0, 0, 0])

    

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
        # animations.append(self._move_to_origin())
        return animations