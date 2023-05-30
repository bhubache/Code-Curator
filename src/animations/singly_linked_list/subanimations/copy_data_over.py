from __future__ import annotations

from typing import TYPE_CHECKING

from custom_logging.custom_logger import CustomLogger
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from data_structures.nodes.singly_linked_list_node import SLLNode
from data_structures.pointers.pointer import Pointer
from data_structures.element import Element
from animations.singly_linked_list.subanimations.fade_out_mobject import FadeOutMobject
from manim import Line
from manim import smooth
from manim import Transform

from .leaf_subanimation import LeafSubanimation
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from data_structures.singly_linked_list import SinglyLinkedList


class CopyDataOver(LeafSubanimation):
    def __init__(
        self,
        sll: SinglyLinkedList,
        from_node: SLLNode,
        to_node: SLLNode,
    ) -> None:
        super().__init__(sll)
        self._from_node: SLLNode = from_node
        self._to_node: SLLNode = to_node
        self._fade_out_data_animation = None
        self._copy_value_path = None
        self._from_node_data_copy: Element = self._from_node.mobj_data.copy()

    def begin(self) -> None:
        self._fade_out_data_animation = FadeOutMobject(self._sll, mobject=self._to_node.mobj_data, parent_mobject=self._to_node.container)
        self._fade_out_data_animation.begin()

        self._to_node.container.add(self._from_node_data_copy)
        self._copy_value_path = Line(
            start=self._from_node.mobj_data.get_center(),
            end=self._to_node.mobj_data.get_center(),
        )

        # self._original_state = self._node.mobj_data.copy()
        # self._sll.add(self._pointer)
        # self._path = Line(start=self._pointer.end, start=self._pointer.start)

    def interpolate(self, alpha: float) -> None:
        self._fade_out_data_animation.interpolate(alpha)
        # self._to_node.mobj_data.set_opacity(1 - smooth(alpha))
        self._from_node_data_copy.move_to(self._copy_value_path.point_from_proportion(smooth(alpha)))
        # self._from_node.mobj_data.move_to(self._copy_value_path.point_from_proportion(smooth(alpha)))

        # self._node.mobj_data.become(self._original_state)
        # transform = Transform(self._node.mobj_data, self._new_data)
        # transform.begin()
        # transform.interpolate(smooth(alpha))
        # try:
        #     self._node.mobj_data.move_to(
        #         [self._node.get_container_center()[0], self._node.next.get_container_center()[1], self._node.get_container_center()[2]]
        #     )
        # except AttributeError:
        #     raise NotImplementedError('Getting the previous node is not yet implemented')

        # self._node.mobj_data.move_to(self._node.next.container)
        # self._node.mobj_data.move_to(self._node.get_container_center())

    def clean_up_from_animation(self) -> None:
        print('!!!!!!!!!!!!!!!!!!')
        print('!!!!!!!!!!!!!!!!!!')
        print('!!!!!!!!!!!!!!!!!!')
        print('!!!!!!!!!!!!!!!!!!')
        print('!!!!!!!!!!!!!!!!!!')
        print('!!!!!!!!!!!!!!!!!!')
        print('!!!!!!!!!!!!!!!!!!')
        super().clean_up_from_animation()
        # self._to_node.container.remove(self._to_node.mobj_data)
        # self._to_node.remove(self._to_node.mobj_data)
        print(self._to_node.container.submobjects)
        self._to_node.mobj_data = self._copy_value_path
        self._fade_out_data_animation.clean_up_from_animation()

    def clean_up_from_scene(self, scene):
        super().clean_up_from_scene(scene)
        self._fade_out_data_animation.clean_up_from_scene(scene)

    def create_successive_counterpart(self) -> LeafSubanimation:
        return self
