import numpy as np

from .leaf_subanimation import LeafSubanimation
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from data_structures.nodes.singly_linked_list_node import SLLNode
from data_structures.pointers.pointer import Pointer
from .strictly_successive.shift_sub_list import SuccessiveShiftSubList
from manim import VGroup, smooth, LEFT, DOWN, RIGHT, Circle, Mobject, Line

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class ShiftSubList(LeafSubanimation):
    def __init__(self, sll, sub_list_to_shift: VGroup, index: int):
        super().__init__(sll)
        self._sub_list_to_shift: VGroup = sub_list_to_shift
        self._index: int = index

        self._sub_list_original_start: np.ndarray = None
        self._group_to_move_to: VGroup = None

    def begin(self):
        # TODO: Account for more than just a horizontal shift!
        self._sub_list_original_start = self._sub_list_to_shift.get_center()
        self._group_to_move_to = VGroup(*[node for i, node in enumerate(self._sll_post_subanimation_group) if i > self._index], self._sll.tail_pointer)
        self._sub_list_to_shift.save_state()

        # TODO: Shorten code by using a line with point_from_proportion

    def interpolate(self, alpha: float):
        self._sub_list_to_shift.restore()
        self._sub_list_to_shift.move_to(self._sub_list_original_start + ((self._group_to_move_to.get_center() - self._sub_list_to_shift.get_center()) * smooth(alpha)))

    def create_successive_counterpart(self) -> LeafSubanimation:
        return SuccessiveShiftSubList(self._sll, self._index)
