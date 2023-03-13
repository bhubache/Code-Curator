from ..base_subanimation import BaseSubanimation
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from manim import smooth

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class SuccessiveGrowPointer(BaseSubanimation):
    def __init__(self, sll, pointer):
        super().__init__(sll)
        self._pointer = pointer
        # self._node = node
    
    def begin(self):
        self._pointer.save_state()
        self._pointer.set_opacity(0)

    def interpolate(self, alpha: float):
        curr_start, curr_end = self._pointer.get_start_and_end()
        self._pointer.restore()

        original_start, original_end = self._pointer.get_start_and_end()
        new_end = [self._pointer.tip.length, 0, 0] + curr_start + ((original_end - original_start - [self._pointer.tip.length, 0, 0]) * [smooth(alpha), 1, 1])
        self._pointer.become(
            SinglyDirectedEdge(
                start=curr_start,
                end=new_end
            )
        )
        self._pointer.set_opacity(alpha)
        # self._save_sll_state()
        # self._pointer.save_state()
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.add(self._pointer)
        # self._save_sll_state()
        self._sll.save_state()