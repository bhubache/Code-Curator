from __future__ import annotations

from custom_logging.custom_logger import CustomLogger
from manim import LEFT
from manim import RIGHT
from manim import smooth

from .leaf_subanimation import LeafSubanimation
from .strictly_successive.center_sll import SuccessiveCenterSLL
logger = CustomLogger.getLogger(__name__)


class CenterSLL(LeafSubanimation):
    def __init__(self, sll, curr_reference_index: int, post_subanimation_reference_index: int):
        super().__init__(sll)
        self._curr_reference_index: int = curr_reference_index
        self._post_subanimation_reference_index: int = post_subanimation_reference_index

    def begin(self):
        logger.info(self._sll.get_left())
        logger.info(self._sll_post_subanimation_group.get_left())
        self._original_left = self._sll.get_left()
        self._begin_center = self._sll.get_center()
        self._shift_distance = self._sll_post_subanimation_group.get_left() - \
            self._sll.get_left()

        logger.info(self._shift_distance)

        # self._sll.add(Circle(radius=0.02).move_to(self._sll.get_left()).set_color(BLUE))
        # self._sll.add(Circle(radius=0.02).move_to(self._sll_post_subanimation_group.get_left()))

        self._shift_direction = None

        self._curr_left_x = self._sll[self._curr_reference_index].get_left()[0]
        self._post_subanimation_left_x = self._sll_post_subanimation_group[
            self._post_subanimation_reference_index
        ].get_left()[0]

        if self._curr_left_x < self._post_subanimation_left_x:
            self._shift_direction = LEFT
        elif self._curr_left_x > self._post_subanimation_left_x:
            self._shift_direction = RIGHT
        else:
            self._shift_direction = [0, 0, 0]

        # self._shift_distance = self._get_corrected_shift_distance()

    def interpolate(self, alpha: float):
        self._sll.align_to(self._original_left, LEFT)
        self._sll.shift(
            self._shift_direction *
            self._shift_distance * smooth(alpha),
        )

    def clean_up_from_animation(self):
        super().clean_up_from_animation()

    def create_successive_counterpart(self) -> LeafSubanimation:
        return SuccessiveCenterSLL(self._sll)

    # def _get_corrected_shift_distance(self) -> np.ndarray:
    #     sll_copy = self._sll.copy()
    #     sll_copy.shift(self._shift_direction * self._shift_distance * 1)

    #     origin = [0, 0, 0]

    #     corrected_shift_distance = origin
    #     if not self._positions_equal(sll_copy.get_center(), origin):
    #         corrected_shift_distance = self._shift_distance - (sll_copy.get_center() - origin)
    #     return corrected_shift_distance

    # def _positions_equal(self, pos_one: np.ndarray, pos_two: np.ndarray) -> bool:
    #     for component_first, component_second in zip(pos_one, pos_two):
    #         if component_first != component_second:
    #             return False
    #     return True
