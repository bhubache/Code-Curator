from .leaf_subanimation import LeafSubanimation
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from manim import Scene, Mobject, Line, smooth

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class CurvePointer(LeafSubanimation):
    def __init__(self, sll, pointer, start_node, new_end_node):
        super().__init__(sll)
        self._pointer = pointer
        self._start_node = start_node
        self._new_end_node = new_end_node

    def begin(self):
        self._sll.add(self._pointer)
        # self._path = Line(start=self._pointer.end, start=self._pointer.start)

    def interpolate(self, alpha: float):
        tip_length = self._pointer.tip.length
        pointer_start = self._start_node.get_container_right()
        self._path = Line(start=self._start_node.next.get_container_left(), end=self._new_end_node.get_container_left())
        self._pointer.become(
            SinglyDirectedEdge.create_curved_pointer(
                start=pointer_start,
                end=self._path.point_from_proportion(smooth(alpha)),
                angle=(smooth(alpha) * (1.25 + self._start_node.radius))
            )
        )

    def clean_up_from_animation(self):
        super().clean_up_from_animation()

    def create_successive_counterpart(self) -> LeafSubanimation:
        return CurvePointer(self._sll, self._pointer, self._start_node, self._new_end_node)
