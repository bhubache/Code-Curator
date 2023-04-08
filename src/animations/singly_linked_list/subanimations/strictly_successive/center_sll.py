from ..leaf_subanimation import LeafSubanimation
from data_structures import singly_linked_list
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from manim import smooth, RIGHT, UP, Mobject, Circle, Line

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class SuccessiveCenterSLL(LeafSubanimation):
    def __init__(self, sll):
        super().__init__(sll)

    def begin(self):
        begin_center = self._sll.get_center()
        # TODO: Change hardcoded origin to dynamic origin
        self._sll_path = Line(start=begin_center, end=[0, 0, 0])

    def interpolate(self, alpha: float):
        self._sll.move_to(self._sll_path.point_from_proportion(smooth(alpha)))

    def clean_up_from_animation(self):
        super().clean_up_from_animation()

    def create_successive_counterpart(self) -> LeafSubanimation:
        return SuccessiveCenterSLL(self._sll)
