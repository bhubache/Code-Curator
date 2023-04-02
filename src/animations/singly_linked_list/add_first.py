from typing import Any

from .data_structure_animator import BaseSLLPackager
from .data_structure_animator import assign_subanimations_and_animate
from data_structures.nodes.singly_linked_list_node import SLLNode
from ..animation_package import AnimationPackage
from .subanimations.fade_in_container import FadeInContainer
# from .subanimations.fade_in_pointer import FadeInPointer
from .subanimations.grow_pointer import GrowPointer
from .subanimations.move_trav import MoveTrav
from .subanimations.center_sll import CenterSLL
from .subanimations.empty import Empty
from ..data_structure_animation import PackageAnimation
from manim import LEFT, Animation, linear, smooth, Scene

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

# TODO: Allow specifying the time that each animation should take within this class animation
#       alpha should be scaled accordingly
# TODO: Create unaligned addfirst
# TODO: Create generic adding node animation (not just to front)


class AddFirst(BaseSLLPackager):
    '''
    Handles the internal manipulation and animation of adding a node to the front of a linked list.
    '''
    def __init__(self, sll):
        self._sll = sll

        self._fade_in_container = Empty(self._sll)
        self._pointer_animation = Empty(self._sll)
        self._move_trav = Empty(self._sll)
        self._center_sll = Empty(self._sll)

    def _set_kwargs_defaults(self, **kwargs):
        kwargs.setdefault('aligned', False)
        return kwargs

    def _assign_subanimations(self, index: int, node: SLLNode, *, pointer_animation_type: str, aligned: bool):
        node.container.set_opacity(0)
        node.pointer_to_next.set_opacity(0)
        self._fade_in_container = FadeInContainer(self._sll, node.container)
        self._pointer_animation = self._get_pointer_animation(node, pointer_animation_type)
        self._move_trav = MoveTrav(self._sll, self._sll.head_pointer, node)
        self._center_sll = CenterSLL(self._sll)

        # if aligned:
        #     self._shift_sub_list = ShiftSubList(self._sll, VGroup(*[node for i, node in enumerate(self._sll) if i > index], self._sll.tail_pointer), index)
        #     self._center_sll = CenterSLL(self._sll)
        #     # self._sll[index].pointer_to_next.become(SinglyDirectedEdge(start=self._sll[index].get_container_top(), end=self._sll[index + 1].get_container_bottom()))
        # else:
        #     self._center_sll = CenterSLL(self._sll)

        #     # node.container.next_to(self._sll[index + 1].container, DOWN)
        #     # node.pointer_to_next.become(SinglyDirectedEdge(start=self._sll[index].get_container_top(), end=self._sll[index + 1].get_container_bottom()))
        #     self._change_next_pointer = ChangeNextPointer(self._sll, self._sll[index - 1].pointer_to_next, node)
        #     self._flatten_list = FlattenList(self._sll, index, node)

    #################
    # One animation #
    #################
    @assign_subanimations_and_animate
    def all_together(self, *args, **kwargs):
        self.append_concurrent_animations(
            self._fade_in_container,
            self._pointer_animation,
            self._move_trav,
            self._center_sll
        )

    ##################
    # Two animations #
    ##################
    @assign_subanimations_and_animate
    def node_then_rest(self, *args, **kwargs):
        self.append_concurrent_animations(
            self._fade_in_container
        )
        self.append_concurrent_animations(
            self._pointer_animation,
            self._move_trav,
            self._center_sll
        )

    @assign_subanimations_and_animate
    def node_and_pointer_then_rest(self, *args, **kwargs):
        self.append_concurrent_animations(
            self._fade_in_container,
            self._pointer_animation
        )
        self.append_concurrent_animations(
            self._move_trav,
            self._center_sll
        )

    @assign_subanimations_and_animate
    def node_and_pointer_and_trav_then_rest(self, *args, **kwargs):
        self.append_concurrent_animations(
            self._fade_in_container,
            self._pointer_animation,
            self._move_trav,
        )
        self.append_concurrent_animations(
            self._center_sll
        )

    @assign_subanimations_and_animate
    def node_and_trav_then_rest(self, *args, **kwargs):
        self.append_concurrent_animations(
            self._fade_in_container,
            self._move_trav,
        )
        self.append_concurrent_animations(
            self._pointer_animation,
            self._center_sll
        )

    @assign_subanimations_and_animate
    def node_and_center_then_rest(self, *args, **kwargs):
        self.append_concurrent_animations(
            self._fade_in_container,
            self._center_sll
        )
        self.append_concurrent_animations(
            self._pointer_animation,
            self._move_trav
        )

    ####################
    # Three animations #
    ####################
    @assign_subanimations_and_animate
    def node_then_pointer_then_rest(self, *args, **kwargs):
        self.append_successive_animations(
            self._fade_in_container,
            self._pointer_animation,
        )
        self.append_concurrent_animations(
            self._move_trav,
            self._center_sll
        )

    @assign_subanimations_and_animate
    def node_then_trav_then_rest(self, *args, **kwargs):
        self.append_successive_animations(
            self._fade_in_container,
            self._move_trav,
        )
        self.append_concurrent_animations(
            self._pointer_animation,
            self._center_sll
        )

    @assign_subanimations_and_animate
    def node_then_center_then_rest(self, *args, **kwargs):
        self.append_successive_animations(
            self._fade_in_container,
            self._center_sll
        )
        self.append_concurrent_animations(
            self._move_trav,
            self._pointer_animation,
        )

    ###################
    # Four animations #
    ###################
    @assign_subanimations_and_animate
    def node_then_pointer_then_trav_then_center(self, *args, **kwargs):
        self.append_successive_animations(
            self._fade_in_container,
            self._pointer_animation,
            self._move_trav,
            self._center_sll,
        )

    @assign_subanimations_and_animate
    def node_then_trav_then_pointer_then_center(self, *args, **kwargs):
        self.append_successive_animations(
            self._fade_in_container,
            self._move_trav,
            self._pointer_animation,
            self._center_sll,
        )

    @assign_subanimations_and_animate
    def node_then_center_then_pointer_then_trav(self, *args, **kwargs):
        self.append_successive_animations(
            self._fade_in_container,
            self._center_sll,
            self._pointer_animation,
            self._move_trav,
        )

    @assign_subanimations_and_animate
    def node_then_center_then_trav_then_pointer(self, *args, **kwargs):
        self.append_successive_animations(
            self._fade_in_container,
            self._center_sll,
            self._move_trav,
            self._pointer_animation,
        )

    @assign_subanimations_and_animate
    def center_then_node_then_pointer_then_trav(self, *args, **kwargs):
        self.append_successive_animations(
            self._center_sll,
            self._fade_in_container,
            self._pointer_animation,
            self._move_trav,
        )

    @assign_subanimations_and_animate
    def center_then_node_then_trav_then_pointer(self, *args, **kwargs):
        self.append_successive_animations(
            self._center_sll,
            self._fade_in_container,
            self._move_trav,
            self._pointer_animation,
        )


    # TODO: Finish the remaining animations
