from __future__ import annotations


from data_structures.nodes.singly_linked_list_node import SLLNode

from ..data_structure_animation import PackageAnimation
from .data_structure_animator import assign_subanimations_and_animate
from .data_structure_animator import BaseSLLPackager
from .subanimations.center_sll import CenterSLL
from .subanimations.empty import Empty
from .subanimations.fade_out_container import FadeOutContainer
from .subanimations.fade_out_mobject import FadeOutMobject
from .subanimations.move_trav import MoveTrav


class RemoveLast(BaseSLLPackager):
    def __init__(self, sll):
        self._sll = sll

        self._fade_out_container = Empty(self._sll)
        self._fade_out_pointer = Empty(self._sll)
        self._move_trav = Empty(self._sll)
        self._center_sll = Empty(self._sll)

    def _set_kwargs_defaults(self, **kwargs) -> dict:
        return kwargs

    def _assign_subanimations(self, index: int, node: SLLNode):
        self._fade_out_container = FadeOutContainer(
            self._sll, node.container, node,
        )
        self._fade_out_pointer = FadeOutMobject(
            self._sll, self._sll[index - 1].pointer_to_next, self._sll[index - 1],
        )
        self._move_trav = MoveTrav(
            self._sll, self._sll.tail_pointer, self._sll._tail,
        )
        self._center_sll = CenterSLL(
            self._sll, curr_reference_index=len(
            self._sll,
            ) - 1, post_subanimation_reference_index=len(self._sll) - 2,
        )

    @assign_subanimations_and_animate
    def all_together(self, *args, **kwargs) -> PackageAnimation:
        self.append_concurrent_animations(
            self._fade_out_container,
            self._fade_out_pointer,
            self._move_trav,
            self._center_sll,
        )
