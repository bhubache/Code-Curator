from typing import Any

# from data_structures.singly_linked_list.singly_linked_list import SinglyLinkedList
from .data_structure_animator import BaseSLLPackager
from .data_structure_animator import assign_subanimations_and_animate
from data_structures.nodes.singly_linked_list_node import SLLNode
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from data_structures.nodes.singly_linked_list_node import SLLNode
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from data_structures.pointers.pointer import Pointer
from .subanimations.base_subanimation import BaseSubanimation
from ..animation_package import AnimationPackage
from ..data_structure_animation import PackageAnimation
from .subanimations.fade_in_container import FadeInContainer
from .subanimations.fade_in_mobject import FadeInMobject
from .subanimations.fade_out_mobject import FadeOutMobject
# from .subanimations.fade_in_pointer import FadeInPointer
from .subanimations.grow_pointer import GrowPointer
from .subanimations.move_trav import MoveTrav
from .subanimations.center_sll import CenterSLL
from .subanimations.change_next_pointer import ChangeNextPointer
from .subanimations.flatten_tail import FlattenTail
# from .subanimations.fade_in_trav import FadeInTrav
# from .subanimations.fade_out_trav import FadeOutTrav
from .subanimations.shift_sub_list import ShiftSubList
from .subanimations.strictly_successive.shift_sub_list import SuccessiveShiftSubList
from .subanimations.strictly_successive.center_sll import SuccessiveCenterSLL
from .subanimations.empty import Empty
from manim import RIGHT, UP, Animation, linear, smooth, Scene, Circle, VGroup

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

# The following imports are for development
from .subanimations.fade_in_container import FadeInContainer
# from .subanimations.fade_in_pointer import FadeInPointer
from animations.animation_package import AnimationPackage


class AddLast(BaseSLLPackager):
    def __init__(self, sll):
        self._sll = sll
        self._trav = Circle().set_opacity(0)
        self._added_node = None

        self._fade_in_container = Empty(self._sll)
        self._pointer_animation = Empty(self._sll)
        self._move_trav = Empty(self._sll)
        self._center_sll = Empty(self._sll)
        self._change_next_pointer = Empty(self._sll)
        self._flatten_tail = Empty(self._sll)
        self._fade_out_temp_trav = Empty(self._sll)
        self._shift_sub_list = Empty(self._sll)
        self._move_head_trav = Empty(self._sll)
        self._move_tail_trav = Empty(self._sll)

    def _set_kwargs_defaults(self, **kwargs):
        kwargs.setdefault('display_trav', False)
        kwargs.setdefault('trav_name', 'trav')
        kwargs.setdefault('trav_position', 'start')
        kwargs.setdefault('aligned', False)
        return kwargs

    def _assign_subanimations(self, index: int, node: SLLNode, pointer_animation_type: str, display_trav: bool, trav_name: str, trav_position: str, aligned: bool):
        self._move_tail_trav = MoveTrav(self._sll, self._sll.tail_pointer, node)
        self._fade_in_container = FadeInContainer(self._sll, node.container)

        # TODO: Make this standardized
        node.container.set_opacity(0)
        self._sll[-2].pointer_to_next.set_opacity(0)
        # FIXME: GrowPointer does a weird movement (though it does end in the correct position)
        self._pointer_animation = self._get_pointer_animation(node=self._sll[index - 1], pointer_animation_type=pointer_animation_type)

        if aligned:
            # self._shift_sub_list = ShiftSubList(self._sll, VGroup(*[node for i, node in enumerate(self._sll) if i > index], self._sll.tail_pointer), index)
            self._center_sll = CenterSLL(self._sll)
        else:
            self._center_sll = CenterSLL(self._sll)
            self._flatten_tail = FlattenTail(self._sll, index, node)

            # node.container.next_to(self._sll[index + 1].container, DOWN)
            # node.pointer_to_next.become(SinglyDirectedEdge(start=self._sll[index].get_container_top(), end=self._sll[index + 1].get_container_bottom()))
            # self._change_next_pointer = ChangeNextPointer(self._sll, self._sll[index - 1].pointer_to_next, node)

        if display_trav:
            trav_starting_node, trav_starting_index = (self._sll[0], 0) if trav_position == 'start' else (self._sll[index - 1], index - 1)
            self._trav = Pointer(trav_starting_node, self._sll, label=trav_name, direction=UP)
            self._animation_package.prepend_successive_animations(
                FadeInMobject(self._sll, self._trav),
                *[
                    MoveTrav(self._sll, self._trav, self._sll[i])
                    for i in range(trav_starting_index + 1, len(self._sll) - 1)
                ]
            )
        self._fade_out_temp_trav = FadeOutMobject(self._sll, self._trav, self._sll)

    @assign_subanimations_and_animate
    def all_together(self, index: int, data) -> PackageAnimation:
        self._animation_package.append_concurrent_animations(
            self._fade_in_container,
            self._pointer_animation,
            self._fade_out_temp_trav,
            self._flatten_tail,
            self._move_tail_trav,
            self._center_sll,
        )



    @assign_subanimations_and_animate
    def add_last_test(
        self,
        index: int,
        data: Any,
        *,
        pointer_animation_type: str,
        display_trav: bool,
        trav_name: str,
        trav_position: str,
        aligned: bool,
        **kwargs
    ) -> PackageAnimation:
        # self._animation_package.append_successive_animations(
        #     self._fade_in_container,
        #     self._pointer_animation,
        #     self._change_next_pointer,
        #     self._fade_out_temp_trav,
        #     self._flatten_tail,
        #     self._center_sll
        # )
        self._animation_package.append_successive_animations(
            self._fade_in_container,
            self._pointer_animation,
            # self._shift_sub_list,
            # self._center_sll
            # self._pointer_animation,
            # self._change_next_pointer,
            # self._flatten_tail,
            self._fade_out_temp_trav,
            self._flatten_tail,
            self._move_tail_trav,
            self._center_sll,
            # self._center_sll
        )
        # self._animation_package.append_successive_animations(
        #     self._change_next_pointer,
        #     self._fade_out_temp_trav,
        # )
        self._animation_package.append_concurrent_animations(
        )
        self._animation_package.append_concurrent_animations(
        )
        # self._animation_package.append_concurrent_animations(
        #     # self._flatten_tail,
        #     self._center_sll
        # )
