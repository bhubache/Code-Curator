from .leaf_subanimation import LeafSubanimation
from manim import Scene, Mobject

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class Empty(LeafSubanimation):
    def __init__(self, sll):
        super().__init__(sll)

    def begin(self):
        pass

    def interpolate(self, alpha: float):
        pass

    def clean_up_from_animation(self):
        pass

    def create_successive_counterpart(self) -> LeafSubanimation:
        return Empty(self._sll)
