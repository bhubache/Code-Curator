from typing import Any

# import data_structures.singly_linked_list.singly_linked_list as 
# from data_structures.singly_linked_list.singly_linked_list import SinglyLinkedList
from ..nodes.singly_linked_list_node import SLLNode as Node
from ..edges.singly_directed_edge import SinglyDirectedEdge
from manim import LEFT, AnimationGroup, Succession, FadeOut, UpdateFromAlphaFunc, FadeIn, Create, Circle, UP
from manim import *

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

# TODO: Allow specifying the time that each animation should take within this class animation
#       alpha should be scaled accordingly


'''
Let's try and list all the possible animation variants
------------------------------------------------------

0 Animation (Immediately add everything to scene)

1 Animation
    1. Quick
        a. Node fades in, pointer fades in (or grows), head pointer moves to new head, everything becomes centered

2 Animations
    1. NodeFirst
        a. Node fades in
        b. Pointer fades in (or grows), head pointer moves, everything centers

    2. NodeAndPointerFirst
        a. Node and pointer fades in (or pointer grows)
        b. Head pointer moves and everything becomes centered

    3. NodeAndPointerAndFlatten
        a. Node and pointer fades in (or pointer grows) but not in line with linked list
        b. Node and pointer flatten, head pointer moves, everything becomes centered

    4. AlignedCenterLast
        a. Node fades in, pointer fades in (or grows), head pointer moves
        b. Everything centers

    5. UnalignedCenterLast
        a. Node fades in, pointer fades in (or grows) (these aren't in line with linked list), head pointer moves, list flattens
        b. Everything centers

3 Animations
    1. Some name
        a. Node fades in
        b. Pointer fades in
        c. Head pointer moves and everything centers

    2. Some name
        a. Node fades in and pointer fades in
        b. Head pointer moves
        c. Everything centers

    3. Some name
        a. Node fades in
        b. pointer fades in, head pointer moves
        c. Everything centers

    4. Some name
        a. Node fades in, pointer fades in (unaligned)
        b. 
'''



class ThreeAnimations(Animation):
    def __init__(
        self,
        sll,
        node,
        run_time = 3,
        rate_func = linear,
        **kwargs
    ):
        super().__init__(sll, run_time=run_time, rate_func=rate_func, **kwargs)
        self.sll = sll
        self.node = node
        self.container = self.node._container
        self.pointer = self.node._pointer_to_next
        self.num_animations = 3
        self.norm = 0.33
        self.upper_alpha_bounds = [val / self.num_animations for val in range(1, self.num_animations + 1)]

    def _get_animation_num(self, alpha: float) -> int:
        for i, upper_alpha in enumerate(self.upper_alpha_bounds):
            if alpha <= upper_alpha:
                return i + 1
        raise RuntimeError(f'Alpha value {alpha} out of bounds for ThreeAnimations AddFirst animation')

    def _get_normalized_alpha(self, rate_func_alpha: float, animation_num: int) -> float:
        normalized_alpha = (rate_func_alpha - (self.norm * (animation_num - 1))) / self.norm
        if normalized_alpha > 1:
            normalized_alpha = 1
        return normalized_alpha

    def begin(self):
        self.pointer.save_state()
        self.sll.save_state()
        self.container.set_opacity(0)
        self.pointer.set_opacity(0)
        super().begin()

    def interpolate_mobject(self, alpha):
        rate_func_alpha = self.rate_func(alpha)

        animation_num = self._get_animation_num(rate_func_alpha)
        normalized_alpha = self._get_normalized_alpha(rate_func_alpha, animation_num)

        if animation_num == 1:
            # print(normalized_alpha)
            self.container.set_stroke(opacity=normalized_alpha)
            for container_sub in self.container.submobjects:
                container_sub.set_opacity(normalized_alpha)
        elif animation_num == 2:
            self.pointer.restore()
            original_start, original_end = self.pointer.get_start_and_end()
            new_end = [self.pointer.tip.length, 0, 0] + original_start + ((original_end - original_start - [self.pointer.tip.length, 0, 0]) * [smooth(normalized_alpha), 1, 1])
            self.pointer.become(SinglyDirectedEdge(start=original_start, end=new_end))
            self.pointer.set_opacity(normalized_alpha)
        elif animation_num == 3:
            self.sll.restore()
            self.sll.move_to([self.sll.get_center()[0] - (self.sll.get_center()[0] * smooth(normalized_alpha)), 0, 0])

            self.sll._head_pointer.move_immediately_alpha(self.node, self.node, smooth(normalized_alpha))
            



    def clean_up_from_scene(self, scene: Scene = None) -> None:
        scene.add(self.node)
        self.node.remove(self.sll)
        super().clean_up_from_scene(scene)
        # self.interpolate(0)


class AddFirst:
    def __init__(self, sll):
        self._sll = sll

    def one_animation(self, data: Any):
        node = Node(data)
        self._sll._place_node_next_to(node, self._sll._head, LEFT)
        node.set_next(self._sll._head)
        self._sll.add(node)
        FadeOut(node)

        def update_sll(mobject, alpha):
            node.fade(1 - alpha)

        self._sll._head = node

        self._sll._nodes.insert(0, node)

        positioned_node = self._sll.copy().move_to([0, 0, 0])._nodes[0]


        return AnimationGroup(
            AnimationGroup(
                self._sll.move_to_origin(),
                UpdateFromAlphaFunc(self._sll, update_sll)
            ),
            self._sll._move_pointer(self._sll._head_pointer, positioned_node, self._sll._nodes[0])
        )

    def two_animations(self, data):
        node = Node(data)
        self._sll._place_node_next_to(node, self._sll._head, LEFT)
        node.set_next(self._sll._head)
        self._sll.add(node)
        FadeOut(node)

        def update_sll(mobject, alpha):
            node.fade(1 - alpha)

        self._sll._head = node

        self._sll._nodes.insert(0, node)

        positioned_node = self._sll.copy().move_to([0, 0, 0])._nodes[0]


        return Succession(
            AnimationGroup(
                self._sll.move_to_origin(),
                UpdateFromAlphaFunc(self._sll, update_sll)
            ),
            self._sll._move_pointer(self._sll._head_pointer, positioned_node, self._sll._nodes[0])
        )

    def three_animations(self, data):
        # node = self._add_first(data)
        node = Node(data)
        node.next_to(self._sll._head, LEFT, buff=1)
        node.set_next(self._sll._head)

        node.add(node._pointer_to_next)
        node.add(node._container)

        logger.info(self._sll.submobjects)

        self._sll._nodes.insert(0, node)
        self._sll.add(node)

        self._sll._head = node



        # self._sll.move_to([0, 2, 0])

        # self._sll.remove(node)

        # node._container.fade(0.9)
        # node._pointer_to_next.fade(0)

        # node.remove(node._container)
        # node.remove(node._pointer_to_next)

        s = Square()
        s._container = None
        s._pointer_to_next = None

        # return Succession(
        #     Transform(self._sll, self._sll.copy().move_to([1, 0, 0])),
        #     Transform(self._sll, self._sll.copy().move_to([-1, 0, 0])),
        #     Transform(self._sll, self._sll.copy().move_to([1, 1, 0]))
        # )

        # return ThreeAnimations(node, self._sll)
        return ThreeAnimations(self._sll, node)

        sq = Square().scale(2)
        self._sll.add(sq)

        return Succession(
            UpdateFromAlphaFunc(sq, move_square_multiple_times),
            run_time=5
            # sq.animate.move_to([0, 2, 0]),
            # sq.animate.move_to([1, -1, 0]),
            # sq.animate.move_to([-1, 0, 0]),
            # UpdateFromAlphaFunc(node, lambda mob, alpha : mob._container.fade(1 - alpha)),
            # UpdateFromAlphaFunc(node, lambda mob, alpha : mob._pointer_to_next.fade(1 - alpha)),
            # node._pointer_to_next.animate.fade(0),
            # node.animate_fade_in_container(),
            # node.animate_fade_in_pointer(),
            # self._sll.animate.move_to([0, 2, 0]),
            # self._sll.animate.move_to([1, -2, 0]),
            # Create(Circle(radius=0.01).move_to(self._sll.get_left())),
            # self._sll._move_pointer(self._sll._head_pointer, self._sll._nodes[0], self._sll._nodes[0]),
            # self._sll.move_to_origin(),
        )

    def four_animations(self):
        pass

    
    def _add_first(self, data: Any) -> Node:
        node = Node(data)
        self._sll._place_node_next_to(node, self._sll._head, LEFT)
        node.set_next(self._sll._head)

        self._sll._head = node
        self._sll._nodes.insert(0, node)
        self._sll.add(node)
        return node
