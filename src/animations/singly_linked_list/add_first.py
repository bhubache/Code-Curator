from typing import Any

from data_structures.nodes.singly_linked_list_node import SLLNode
from ..animation_package import AnimationPackage
from .subanimations.fade_in_node import FadeInNode
from .subanimations.fade_in_pointer import FadeInPointer
from .subanimations.grow_pointer import GrowPointer
from .subanimations.move_trav import MoveTrav
from .subanimations.center_sll import CenterSLL
from ..package_animation import PackageAnimation
from manim import LEFT, Animation, linear, smooth, Scene

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

# TODO: Allow specifying the time that each animation should take within this class animation
#       alpha should be scaled accordingly
# TODO: Create unaligned addfirst
# TODO: Create generic adding node animation (not just to front)


class AddFirst:
    '''
    Handles the internal manipulation and animation of adding a node to the front of a linked list.
    '''
    def __init__(self, sll):
        self._sll = sll

        self._animation_package = AnimationPackage(self._sll)
        self._fade_in_node = None
        self._pointer_animation = None
        self._move_trav = None
        self._center_sll = None

    def _assign_subanimations_and_animate(fn):
        def inner(self, *args, **kwargs):
            self._animation_package = AnimationPackage(self._sll)
            self._assign_subanimations(*args, **kwargs)
            fn(self, *args, **kwargs)
            return PackageAnimation(self._sll, self._animation_package)
        return inner
    
    def _assign_subanimations(self, added_node: SLLNode, pointer_animation_type: str):
        self._fade_in_node = FadeInNode(self._sll, added_node)
        pointer_animation_cls = GrowPointer if pointer_animation_type == 'grow' else FadeInPointer
        self._pointer_animation = pointer_animation_cls(self._sll, added_node.pointer_to_next)
        self._move_trav = MoveTrav(self._sll, self._sll.head_pointer, added_node)
        self._center_sll = CenterSLL(self._sll)

    #################
    # One animation #
    #################
    @_assign_subanimations_and_animate
    def all_together(self, added_node: SLLNode, pointer_animation_type: str):
        self._animation_package.append_concurrent_animations(
            self._fade_in_node,
            self._pointer_animation,
            self._move_trav,
            self._center_sll
        )

    ##################
    # Two animations #
    ##################
    @_assign_subanimations_and_animate
    def node_then_rest(self, added_node: SLLNode, pointer_animation_type: str):
        self._animation_package.append_concurrent_animations(
            self._fade_in_node
        )
        self._animation_package.append_concurrent_animations(
            self._pointer_animation,
            self._move_trav,
            self._center_sll
        )

    @_assign_subanimations_and_animate
    def node_and_pointer_then_rest(self, added_node: SLLNode, pointer_animation_type: str):
        self._animation_package.append_concurrent_animations(
            self._fade_in_node,
            self._pointer_animation
        )
        self._animation_package.append_concurrent_animations(
            self._move_trav,
            self._center_sll
        )

    @_assign_subanimations_and_animate
    def node_and_pointer_and_trav_then_rest(self, added_node: SLLNode, pointer_animation_type: str):
        self._animation_package.append_concurrent_animations(
            self._fade_in_node,
            self._pointer_animation,
            self._move_trav,
        )
        self._animation_package.append_concurrent_animations(
            self._center_sll
        )

    @_assign_subanimations_and_animate
    def node_and_trav_then_rest(self, added_node: SLLNode, pointer_animation_type: str):
        self._animation_package.append_concurrent_animations(
            self._fade_in_node,
            self._move_trav,
        )
        self._animation_package.append_concurrent_animations(
            self._pointer_animation,
            self._center_sll
        )

    @_assign_subanimations_and_animate
    def node_and_center_then_rest(self, added_node: SLLNode, pointer_animation_type: str):
        self._animation_package.append_concurrent_animations(
            self._fade_in_node,
            self._center_sll
        )
        self._animation_package.append_concurrent_animations(
            self._pointer_animation,
            self._move_trav
        )

    ####################
    # Three animations #
    ####################
    @_assign_subanimations_and_animate
    def node_then_pointer_then_rest(self, added_node: SLLNode, pointer_animation_type: str):
        self._animation_package.append_concurrent_animations(
            self._fade_in_node,
        )
        self._animation_package.append_concurrent_animations(
            self._pointer_animation,
        )
        self._animation_package.append_concurrent_animations(
            self._move_trav,
            self._center_sll
        )

    @_assign_subanimations_and_animate
    def node_then_trav_then_rest(self, added_node: SLLNode, pointer_animation_type: str):
        self._animation_package.append_concurrent_animations(
            self._fade_in_node,
        )
        self._animation_package.append_concurrent_animations(
            self._move_trav,
        )
        self._animation_package.append_concurrent_animations(
            self._pointer_animation,
            self._center_sll
        )

    @_assign_subanimations_and_animate
    def node_then_center_then_rest(self, added_node: SLLNode, pointer_animation_type: str):
        self._animation_package.append_concurrent_animations(
            self._fade_in_node,
        )
        self._animation_package.append_concurrent_animations(
            self._center_sll
        )
        self._animation_package.append_concurrent_animations(
            self._move_trav,
            self._pointer_animation,
        )

    ###################
    # Four animations #
    ###################
    @_assign_subanimations_and_animate
    def node_then_pointer_then_trav_then_center(self, added_node: SLLNode, pointer_animation_type: str):
        self._animation_package.append_concurrent_animations(
            self._fade_in_node
        )
        self._animation_package.append_concurrent_animations(
            self._pointer_animation
        )
        self._animation_package.append_concurrent_animations(
            self._move_trav
        )
        self._animation_package.append_concurrent_animations(
            self._center_sll
        )

    @_assign_subanimations_and_animate
    def node_then_trav_then_pointer_then_center(self, added_node: SLLNode, pointer_animation_type: str):
        self._animation_package.append_concurrent_animations(
            self._fade_in_node
        )
        self._animation_package.append_concurrent_animations(
            self._move_trav
        )
        self._animation_package.append_concurrent_animations(
            self._pointer_animation
        )
        self._animation_package.append_concurrent_animations(
            self._center_sll
        )

    @_assign_subanimations_and_animate
    def node_then_center_then_pointer_then_trav(self, added_node: SLLNode, pointer_animation_type: str):
        self._animation_package.append_concurrent_animations(
            self._fade_in_node
        )
        self._animation_package.append_concurrent_animations(
            self._center_sll
        )
        self._animation_package.append_concurrent_animations(
            self._pointer_animation
        )
        self._animation_package.append_concurrent_animations(
            self._move_trav
        )

    @_assign_subanimations_and_animate
    def node_then_center_then_trav_then_pointer(self, added_node: SLLNode, pointer_animation_type: str):
        self._animation_package.append_concurrent_animations(
            self._fade_in_node
        )
        self._animation_package.append_concurrent_animations(
            self._center_sll
        )
        self._animation_package.append_concurrent_animations(
            self._move_trav
        )
        self._animation_package.append_concurrent_animations(
            self._pointer_animation
        )

    @_assign_subanimations_and_animate
    def center_then_node_then_pointer_then_trav(self, added_node: SLLNode, pointer_animation_type: str):
        self._animation_package.append_concurrent_animations(
            self._center_sll
        )
        self._animation_package.append_concurrent_animations(
            self._fade_in_node
        )
        self._animation_package.append_concurrent_animations(
            self._pointer_animation
        )
        self._animation_package.append_concurrent_animations(
            self._move_trav
        )

    @_assign_subanimations_and_animate
    def center_then_node_then_trav_then_pointer(self, added_node: SLLNode, pointer_animation_type: str):
        self._animation_package.append_concurrent_animations(
            self._center_sll
        )
        self._animation_package.append_concurrent_animations(
            self._fade_in_node
        )
        self._animation_package.append_concurrent_animations(
            self._move_trav
        )
        self._animation_package.append_concurrent_animations(
            self._pointer_animation
        )


    # TODO: Finish the remaining animations