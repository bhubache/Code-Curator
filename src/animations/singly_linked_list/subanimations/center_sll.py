from .visible_subanimation import VisibleSubanimation
from data_structures.singly_linked_list import singly_linked_list
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from .strictly_successive.center_sll import SuccessiveCenterSLL
from manim import smooth, RIGHT, VGroup

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class CenterSLL(VisibleSubanimation):
    def __init__(self, sll, restore_sll_at_interpolate: bool = False):
        super().__init__(sll)
        self._restore_sll_at_interpolate = restore_sll_at_interpolate
        self._original_center = self._sll.get_center()
        self._original_left = self._sll.get_left()
        self._final_left = self._final_sll.get_left()
        self._begin_center = self._sll.get_center()
        # NOTE: May also need to save self._final_sll
        self._save_states(self._sll)

    def create_successive_counterpart(self):
        return SuccessiveCenterSLL(self._sll, self._restore_sll_at_interpolate)
    
    def _rebind_restored_states(self):
        self._sll = self.restored_states[self._sll]
    
    def begin(self):
        super().begin()
        # self._begin_center = self._sll.get_center()
        self._original_left = self._sll.get_left()
        # self._save_sll_state()
        # NOTE: This is a fix for the sll to start in the correct position
        VGroup(self._sll.head_pointer, *[node for i, node in enumerate(self._sll) if i < 2]).shift(RIGHT)
        self._sll.save_state()
        logger.info(id(self._sll))

    def interpolate(self, alpha: float):
        # if self._restore_sll_at_interpolate:
        #     self._sll.restore()
        #     self._original_center = self._sll.get_center()
        #     self._original_left = self._sll.get_left()
        #     self._restore_sll_at_interpolate = False

        

        shift_right_amount = (self._final_left - self._original_left) * smooth(alpha)
        self._sll.move_to(self._begin_center + shift_right_amount)
        # self._sll.shift(LEFT * smooth(alpha))
        # VGroup(self._sll.head_pointer, *[node for i, node in enumerate(self._sll_post_subanimation_group) if i <= 2]).move_to([-1, -1, 0])
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.head_pointer.save_state()
        self._sll.tail_pointer.save_state()
        self._sll.save_state()
        # self._sll.become(self._sll_post_subanimation_group)
        # self._sll.add(self._pointer)