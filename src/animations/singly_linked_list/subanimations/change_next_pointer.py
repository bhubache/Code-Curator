from .visible_subanimation import VisibleSubanimation
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from .strictly_successive.change_next_pointer import SuccessiveChangeNextPointer
from manim import smooth

class ChangeNextPointer(VisibleSubanimation):
    def __init__(self, sll, pointer, node_to_be_attached):
        super().__init__(sll)
        self._pointer = pointer
        self._node_to_be_attached = node_to_be_attached

    def create_successive_counterpart(self):
        return SuccessiveChangeNextPointer(self._sll, self._pointer, self._node_to_be_attached)

    def begin(self):
        super().begin()
        self._pointer.save_state()

    # NOTE: May have to change start coordinate if SLL is moving
    def interpolate(self, alpha: float):
        self._pointer.restore()
        original_start, original_end = self._pointer.get_start_and_end()
        final_end = original_end + ((self._node_to_be_attached.get_container_left() - original_end) * smooth(alpha))
        self._pointer.become(
            SinglyDirectedEdge(
            start=original_start,
            end=final_end
            )
        )
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.save_state()