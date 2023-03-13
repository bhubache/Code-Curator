from .visible_subanimation import VisibleSubanimation
from .strictly_successive.fade_in_pointer import SuccessiveFadeInPointer
from manim import Scene

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class FadeInPointer(VisibleSubanimation):
    def __init__(self, sll, pointer):
        super().__init__(sll)
        self._pointer = pointer
        self._save_states(self._sll, self._pointer)

    def create_successive_counterpart(self):
        return SuccessiveFadeInPointer(self._sll, self._pointer)
    
    def _rebind_restored_states(self):
        self._sll = self.restored_states[self._sll]
        self._pointer = self.restored_states[self._pointer]
    
    def begin(self):
        super().begin()
        self._sll.add(self._pointer)
        self._pointer.set_opacity(0)
        logger.info(id(self._sll))

    def interpolate(self, alpha: float):
        self._pointer.set_opacity(alpha)
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.add(self._pointer)
        # self._save_sll_state()
        self._sll.save_state()