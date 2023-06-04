from .leaf_subanimation import LeafSubanimation
from code_curator.data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from .strictly_successive.grow_pointer import SuccessiveGrowPointer
from manim import smooth

from code_curator.custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class GrowPointer(LeafSubanimation):
    def __init__(self, sll, pointer):
        super().__init__(sll)
        self._pointer = pointer
        # self._save_states(self._sll, self._pointer)

    def create_successive_counterpart(self) -> LeafSubanimation:
        return SuccessiveGrowPointer(self._sll, self._pointer)

    # def _rebind_restored_states(self):
    #     self._sll = self.restored_states[self._sll]
    #     self._pointer = self.restored_states[self._pointer]

    def begin(self):
        super().begin()
        self._pointer.set_opacity(0)
        self._pointer.save_state()

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
        super().clean_up_from_animation()
