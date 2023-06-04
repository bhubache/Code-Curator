from __future__ import annotations

from custom_logging.custom_logger import CustomLogger
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from manim import LEFT
from manim import Line
from manim import smooth
from manim import VGroup

from ..leaf_subanimation import LeafSubanimation
logger = CustomLogger.getLogger(__name__)


class SuccessiveFlattenListForRemove(LeafSubanimation):
    def __init__(self, sll, start_node, end_node, pointer_to_straighten: SinglyDirectedEdge, sub_list_to_shift: VGroup):
        super().__init__(sll)
        self._start_node = start_node
        self._end_node = end_node
        self._pointer_to_straighten = pointer_to_straighten
        self._sub_list_to_shift = sub_list_to_shift

    def begin(self):
        self._path = Line(
            start=self._start_node.next.get_container_left(
            ), end=self._end_node.get_container_left(),
        )

    def interpolate(self, alpha: float):
        pointer_start = self._start_node.get_container_right()
        new_end = self._path.point_from_proportion(smooth(1 - alpha))

        self._pointer_to_straighten.become(
            SinglyDirectedEdge.create_curved_pointer(
                start=pointer_start,
                end=new_end,
                angle=(smooth(1 - alpha) * (1.25 + self._start_node.radius)),
            ),
        )

        self._sub_list_to_shift.align_to(new_end, LEFT)

    def clean_up_from_animation(self):
        self._pointer_to_straighten.become(
            SinglyDirectedEdge(
                start=self._start_node.get_container_right(),
                end=self._path.point_from_proportion(smooth(0)),
            ),
        )
        self._sub_list_to_shift.align_to(
            self._path.point_from_proportion(smooth(0)), LEFT,
        )
        super().clean_up_from_animation()

    def create_successive_counterpart(self) -> LeafSubanimation:
        return SuccessiveFlattenListForRemove(self._sll, self._index, self._added_node)
