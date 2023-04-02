from .leaf_subanimation import LeafSubanimation
from data_structures.singly_linked_list import singly_linked_list
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from .strictly_successive.center_sll import SuccessiveCenterSLL
from manim import smooth, RIGHT, LEFT, UP, VGroup, Mobject, Line

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)


class CenterSLL(LeafSubanimation):
    def __init__(self, sll, curr_reference_index: int, post_subanimation_reference_index: int):
        super().__init__(sll)
        self._curr_reference_index: int = curr_reference_index
        self._post_subanimation_reference_index: int = post_subanimation_reference_index

    def begin(self):
        self._original_left = self._sll.get_left()
        self._begin_center = self._sll.get_center()
        self._shift_distance = self._sll_post_subanimation_group.get_left() - self._sll.get_left()

        self._shift_direction = None

        self._curr_left_x = self._sll[self._curr_reference_index].get_left()[0]
        self._post_subanimation_left_x = self._sll_post_subanimation_group[self._post_subanimation_reference_index].get_left()[0]

        if self._curr_left_x < self._post_subanimation_left_x:
            self._shift_direction = LEFT
        elif self._curr_left_x > self._post_subanimation_left_x:
            self._shift_direction = RIGHT
        else:
            self._shift_direction = [0, 0, 0]

    def interpolate(self, alpha: float):
        self._sll.align_to(self._original_left, LEFT)
        # self._sll.shift(self._shift_direction * self._shift_distance * smooth(alpha))
        self._sll.shift(self._shift_direction * self._shift_distance * smooth(alpha))

    def clean_up_from_animation(self):
        super().clean_up_from_animation()

    def create_successive_counterpart(self) -> LeafSubanimation:
        return SuccessiveCenterSLL(self._sll)
