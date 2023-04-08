from .leaf_subanimation import LeafSubanimation
from data_structures import singly_linked_list
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from .strictly_successive.move_trav import SuccessiveMoveTrav
from manim import smooth, LEFT, BLUE

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class MoveTrav(LeafSubanimation):
    def __init__(self, sll, trav, to_node):
        super().__init__(sll)
        self._trav = trav
        self._to_node = to_node

    def create_successive_counterpart(self) -> LeafSubanimation:
        return SuccessiveMoveTrav(self._sll, self._trav, self._to_node)

    def begin(self):
        self._trav.save_state()

    def interpolate(self, alpha: float):
        self._trav.restore()
        # self._trav.move_immediately_alpha(self.sll_post_subanimation_group[self._sll._nodes.index(self._to_node)], self._to_node, smooth(alpha))
        self._trav.move_immediately_alpha(self.finished_subanimation._to_node, self._to_node, smooth(alpha))

    def clean_up_from_animation(self):
        self._sll.become(
            self.sll_post_subanimation_group
        )
        self._sll.add(self._trav)
        super().clean_up_from_animation()
