from .leaf_subanimation import LeafSubanimation
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from manim import Scene, Mobject, Line, smooth

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class ShrinkPointer(LeafSubanimation):
    def __init__(self, sll, pointer, node):
        super().__init__(sll)
        self._pointer = pointer
        self._node = node

    def begin(self):
        self._sll.add(self._pointer)
        # self._path = Line(start=self._pointer.end, start=self._pointer.start)

    def interpolate(self, alpha: float):
        pointer_start = self._node.get_container_right()
        self._path = Line(start=pointer_start, end=self._node.next.get_container_left())
        tip_length = self._pointer.tip.length
        self._pointer.become(
            SinglyDirectedEdge(
            start=pointer_start,
            end=self._path.point_from_proportion(1 - smooth(alpha)) + [tip_length * smooth(alpha), 0, 0]
            )
        )

    def clean_up_from_animation(self):
        super().clean_up_from_animation()

    def create_successive_counterpart(self) -> LeafSubanimation:
        return ShrinkPointer(self._sll, self._pointer, self._node)
