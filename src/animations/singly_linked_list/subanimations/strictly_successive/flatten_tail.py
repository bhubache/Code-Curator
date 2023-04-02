import math

from ..leaf_subanimation import LeafSubanimation
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from data_structures.nodes.singly_linked_list_node import SLLNode
from data_structures.pointers.pointer import Pointer
from manim import VGroup, smooth, LEFT, Mobject, Line

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class SuccessiveFlattenTail(LeafSubanimation):
    def __init__(self, sll, index: int, added_node: SLLNode):
        super().__init__(sll)
        self._index: int = index
        self._added_node: SLLNode = added_node
        self._sub_list_to_shift: VGroup = VGroup(*[node for i, node in enumerate(self._sll) if i > self._index], self._sll.tail_pointer)

        self._added_node_original_start = None
        self._total_node_shift_up_distance = None
        self._sub_list_original_start = None
        self._final_sll_copy = None
        self._sub_list_total_distance = None

    def begin(self):
        self._added_node_original_start = self._added_node.container.get_center()
        self._total_node_shift_up_distance = abs((self._added_node.get_container_top() - self._final_sll[self._index].get_container_top())[1])

        # TODO: Account for more than just a horizontal shift!
        # self._sub_list_original_start = self._sub_list_to_shift.get_center()
        # self._final_sll_copy = self._final_sll.copy().align_to(self._sll, LEFT)
        # self._sub_list_total_distance = abs(self._sub_list_to_shift[0].get_left() - self._final_sll_copy[self._index + 1].get_left())

    def interpolate(self, alpha: float):
        self._added_node.container.move_to(self._added_node_original_start + ([0, self._total_node_shift_up_distance * smooth(alpha), 0]))

        # self._sub_list_to_shift.move_to(self._sub_list_original_start + (self._sub_list_total_distance * smooth(alpha)))

        self._sll[self._index - 1].pointer_to_next.become(
            SinglyDirectedEdge(
                start=self._sll[self._index - 1].get_container_right(),
                end=self._added_node.get_container_left()
            )
        )

    def clean_up_from_animation(self):
        super().clean_up_from_animation()

    def create_successive_counterpart(self) -> LeafSubanimation:
        return SuccessiveFlattenTail(self._sll, self._index, self._added_node)
