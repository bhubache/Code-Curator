import math

from .leaf_subanimation import LeafSubanimation
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from data_structures.nodes.singly_linked_list_node import SLLNode
from data_structures.pointers.pointer import Pointer
from .strictly_successive.flatten_list_for_remove import SuccessiveFlattenListForRemove
from manim import VGroup, smooth, LEFT, Mobject, Line

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class FlattenListForRemove(LeafSubanimation):
    def __init__(self, sll, start_node, end_node, pointer_to_straighten: SinglyDirectedEdge, sub_list_to_shift: VGroup):
        super().__init__(sll)
        self._start_node = start_node
        self._end_node = end_node
        self._pointer_to_straighten = pointer_to_straighten
        self._sub_list_to_shift = sub_list_to_shift

    def begin(self):
        self._path = Line(start=self._end_node.get_container_left(), end=self._sll_post_subanimation_group[self._sll._nodes.index(self._end_node)].get_container_left())

    def interpolate(self, alpha: float):
        pointer_start = self._start_node.get_container_right()
        new_end = self._path.point_from_proportion(smooth(alpha))

        self._pointer_to_straighten.become(
            SinglyDirectedEdge.create_curved_pointer(
                start=pointer_start,
                end=new_end,
                angle=(smooth(1 - alpha) * (1.25 + self._start_node.radius))
            )
        )

        self._sub_list_to_shift.align_to(new_end, LEFT)

    def clean_up_from_animation(self):
        self._pointer_to_straighten.become(
            SinglyDirectedEdge(
            start=self._start_node.get_container_right(),
            end=self._path.point_from_proportion(smooth(1))
            )
        )
        self._sub_list_to_shift.align_to(self._path.point_from_proportion(smooth(1)), LEFT)
        super().clean_up_from_animation()

    def create_successive_counterpart(self) -> LeafSubanimation:
        return SuccessiveFlattenListForRemove(self._sll, self._start_node, self._end_node, self._pointer_to_straighten, self._sub_list_to_shift)