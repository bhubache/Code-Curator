from ..base_subanimation import BaseSubanimation
from data_structures.singly_linked_list import singly_linked_list
from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from manim import smooth, LEFT

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class SuccessiveMoveTrav(BaseSubanimation):
    def __init__(self, sll, trav, to_node):
        super().__init__(sll)
        self._trav = trav
        self._to_node = to_node
    
    def begin(self):
        super().begin()
        self._trav.save_state()

    def interpolate(self, alpha: float):
        self._trav.restore()
        self._trav.move_immediately_alpha(self._to_node, self._to_node, smooth(alpha))
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.add(self._trav)
        # self._save_sll_state()
        self._sll.save_state()
