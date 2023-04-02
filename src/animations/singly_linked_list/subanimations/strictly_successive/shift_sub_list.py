from ..leaf_subanimation import LeafSubanimation
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from data_structures.nodes.singly_linked_list_node import SLLNode
from data_structures.pointers.pointer import Pointer
from manim import VGroup, smooth, LEFT, DOWN, RIGHT, Circle, Mobject

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class SuccessiveShiftSubList(LeafSubanimation):
    def __init__(self, sll, index: int):
        super().__init__(sll)
        self._index: int = index
        self._sub_list_to_shift: VGroup = VGroup(*[node for i, node in enumerate(self._sll) if i > self._index], self._sll.tail_pointer)

        # TODO: Account for more than just a horizontal shift!
        self._sub_list_original_start = self._sub_list_to_shift.get_center()
        self._final_sll_copy = self._final_sll.copy().align_to(self._sll, LEFT)
        self._sub_list_total_distance = abs(self._sub_list_to_shift[0].get_left() - self._final_sll_copy[self._index + 1].get_left())

    def begin(self):
        # self._sll.add(self._sub_list_to_shift)
        self._sll.save_state()
        self._sub_list_to_shift.save_state()

    def interpolate(self, alpha: float):
        self._sub_list_to_shift.move_to(self._sub_list_original_start + (self._sub_list_total_distance * smooth(alpha)))

    def clean_up_from_animation(self):
        super().clean_up_from_animation()
        self._sub_list_to_shift.save_state()

    def create_successive_counterpart(self, mobject_map: dict[str, Mobject] = None) -> LeafSubanimation:
        return SuccessiveShiftSubList(self._sll, self._index)
