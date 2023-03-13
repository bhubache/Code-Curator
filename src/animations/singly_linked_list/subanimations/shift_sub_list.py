from .visible_subanimation import VisibleSubanimation
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from data_structures.nodes.singly_linked_list_node import SLLNode
from data_structures.pointers.pointer import Pointer
from .strictly_successive.shift_sub_list import SuccessiveShiftSubList
from manim import VGroup, smooth, LEFT, DOWN, RIGHT, Circle

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class ShiftSubList(VisibleSubanimation):
    def __init__(self, sll, index: int):
        super().__init__(sll)
        self._index: int = index
        self._sub_list_to_shift: VGroup = VGroup(*[node for i, node in enumerate(self._sll) if i > self._index], self._sll.tail_pointer)
        self._save_states(self._sll, self._sub_list_to_shift)

        # self._sll_original_center = self._sll.get_center()
        # self._sll_original_left = self._sll.get_left()
        # self._sll_final_left = self._final_sll.get_left()

        # self._added_node_original_start = self._added_node.container.get_center()
        # self._total_node_shift_up_distance = abs((self._added_node.get_container_top() - self._final_sll[self._index].get_container_top())[1])

        # TODO: Account for more than just a horizontal shift!
        self._sub_list_original_start = self._sub_list_to_shift.get_center()
        # self._sub_list_total_distance = None
        # self._final_sll_copy = self._final_sll.copy().align_to(self._sll, LEFT)
        # self._sub_list_total_distance = abs(self._sub_list_to_shift[0].get_left() - self._final_sll[self._index + 1].get_left())
        self._final_sll_copy = self._final_sll.copy().align_to(self._sll, LEFT)
        self._sub_list_total_distance = abs(self._sub_list_to_shift[0].get_left() - self._final_sll_copy[self._index + 1].get_left())

        # self._sub_list_total_distance = abs(self._sub_list_to_shift[0].get_left() - self._sll_post_subanimation_group.get_left())

    def create_successive_counterpart(self):
        return SuccessiveShiftSubList(self._sll, self._index)
    
    def _rebind_restored_states(self):
        self._sll = self.restored_states[self._sll]
        self._sub_list_to_shift = self.restored_states[self._sub_list_to_shift]

    def begin(self):
        super().begin()
        self._sub_list_to_shift.save_state()
        logger.info(id(self._sll))

    def interpolate(self, alpha: float):
        group_to_move_to = VGroup(*[node for i, node in enumerate(self._sll_post_subanimation_group) if i > self._index], self._sll.tail_pointer)
        self._sub_list_to_shift.restore()
        self._sub_list_to_shift.move_to(self._sub_list_original_start + ((group_to_move_to.get_center() - self._sub_list_to_shift.get_center()) * smooth(alpha)))
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.save_state()