from .leaf_subanimation import LeafSubanimation
from .strictly_successive.move_trav import SuccessiveMoveTrav
from ....data_structures.pointers.pointer import Pointer
from ....data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from manim import smooth, Line

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class MoveTrav(LeafSubanimation):
    def __init__(self, sll, trav, to_node):
        super().__init__(sll)
        self._trav = trav
        self._to_node = to_node
        self._trav_start_path = None
        self._trav_end_path = None

    def create_successive_counterpart(self) -> LeafSubanimation:
        return SuccessiveMoveTrav(self._sll, self._trav, self._to_node)

    def begin(self):
        self._trav.save_state()
        trav_final_state = Pointer(
            node=self._to_node,
            sll=self._sll,
            label=self._trav.get_label(),
            direction=self._trav.get_opposite_direction()
        )
        final_state_trav_start, final_state_trav_end = trav_final_state.get_start_and_end()
        initial_state_trav_start, initial_state_trav_end = self._trav.get_start_and_end()
        self._trav_start_path = Line(start=initial_state_trav_start, end=final_state_trav_start)
        self._trav_end_path = Line(start=initial_state_trav_end, end=final_state_trav_end)

    def interpolate(self, alpha: float):
        self._trav.restore()
        self._trav.move(self._to_node, self._to_node)
        new_trav_start = self._trav_start_path.point_from_proportion(smooth(alpha))
        new_trav_end = self._trav_end_path.point_from_proportion(smooth(alpha))
        self._trav.become(
            Pointer(
            node=self._to_node,
            sll=self._sll,
            label=self._trav.get_label(),
            )
        )
        # self._trav.move_immediately_alpha(self.finished_subanimation._to_node, self.finished_subanimation._to_node, smooth(alpha))

    def clean_up_from_animation(self):
        self._sll.add(self._trav)
        super().clean_up_from_animation()
