from .visible_subanimation import VisibleSubanimation
from .strictly_successive.fade_in_node import SuccessiveFadeInNode
from manim import Scene

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class FadeInContainer(VisibleSubanimation):
    def __init__(self, sll, node):
        super().__init__(sll)
        self._node = node
        self._save_states(self._sll, self._node)

    def create_successive_counterpart(self):
        return FadeInContainer(self._sll, self._node)
        # return SuccessiveFadeInNode(self._sll, self._node)
    
    def _rebind_restored_states(self):
        self._sll = self.restored_states[self._sll]
        self._pointer = self.restored_states[self._node]

    def begin(self):
        super().begin()
        self._sll.add(self._node)
        container = self._node.container
        container.set_stroke(opacity=0)
        for submobject in container.submobjects:
            submobject.set_opacity(0)
        logger.info(id(self._sll))

    def interpolate(self, alpha: float):
        container = self._node.container
        container.set_stroke(opacity=alpha)
        for submobject in container.submobjects:
            submobject.set_opacity(alpha)
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.add(self._node)
        # self._save_sll_state()
        self._sll.save_state()