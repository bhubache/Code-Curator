from .leaf_subanimation import LeafSubanimation
from data_structures.singly_linked_list import singly_linked_list
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from .strictly_successive.center_sll import SuccessiveCenterSLL
from manim import smooth, RIGHT, LEFT, UP, VGroup, Mobject, Line

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)


class CenterSLL(LeafSubanimation):
    def __init__(self, sll, curr_reference_index: int, post_subanimation_reference_index: int):
        super().__init__(sll, animates_sll=True)
        self._curr_reference_index: int = curr_reference_index
        self._post_subanimation_reference_index: int = post_subanimation_reference_index

    def begin(self):
        self._original_left = self._sll.get_left()
        self._begin_center = self._sll.get_center()
        self._shift_distance = self._sll_post_subanimation_group.get_left() - self._sll.get_left()

        self._shift_direction = None
        # curr_left_x = self._sll[0].get_left()[0]
        # post_subanimation_left_x = self._sll_post_subanimation_group[0].get_left()[0]

        # logger.info(f'curr_left_x             : {curr_left_x}')
        # logger.info(f'post_subanimation_left_x: {post_subanimation_left_x}')

        # logger.info(f'curr_overall_left_x             : {self._sll.get_left()[0]}')
        # logger.info(f'post_subanimation_overall_left_x: {self._sll_post_subanimation_group.get_left()[0]}')

        # print(len(self._sll))
        # print(len(self._sll_post_subanimation_group))

        # if curr_left_x < post_subanimation_left_x:
        #     self._shift_direction = RIGHT
        # else:
        #     self._shift_direction = LEFT
        # left_x = self._sll[0].get_left()[0]
        # right_x = self._sll[-1].get_right()[0]

        # logger.info(left_x)
        # logger.info(self._sll_post_subanimation_group[0].get_left()[0])
        # if abs(left_x) > abs(right_x):
        #     self._shift_direction = RIGHT
        # else:
        #     self._shift_direction = LEFT

        self._curr_left_x = self._sll[self._curr_reference_index].get_left()[0]
        self._post_subanimation_left_x = self._sll_post_subanimation_group[self._post_subanimation_reference_index].get_left()[0]

        logger.info(self._curr_left_x)
        logger.info(self._post_subanimation_left_x)

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
