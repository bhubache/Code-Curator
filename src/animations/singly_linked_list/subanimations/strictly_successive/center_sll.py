from ..base_subanimation import BaseSubanimation
from data_structures.singly_linked_list import singly_linked_list
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from manim import smooth, RIGHT

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class SuccessiveCenterSLL(BaseSubanimation):
    def __init__(self, sll, restore_sll_at_interpolate: bool = False):
        super().__init__(sll)
        self._restore_sll_at_interpolate = restore_sll_at_interpolate
        self._original_center = self._sll.get_center()
        self._original_left = self._sll.get_left()
        self._final_left = self._final_sll.get_left()
        self._begin_center = None
    
    def begin(self):
        self._begin_center = self._sll.get_center()
        # self._save_sll_state()
        self._sll.save_state()

    def interpolate(self, alpha: float):
        # if self._restore_sll_at_interpolate:
        #     self._sll.restore()
        #     self._original_center = self._sll.get_center()
        #     self._original_left = self._sll.get_left()
        #     self._restore_sll_at_interpolate = False

        shift_right_amount = (self._final_left - self._original_left) * smooth(alpha)
        self._sll.move_to(self._begin_center + shift_right_amount)
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.head_pointer.save_state()
        self._sll.tail_pointer.save_state()
        self._sll.save_state()
        # self._sll.add(self._pointer)