from __future__ import annotations

from code_curator.custom_logging.custom_logger import CustomLogger
from manim import Mobject

from .leaf_subanimation import LeafSubanimation
logger = CustomLogger.getLogger(__name__)


class FadeOutMobject(LeafSubanimation):
    def __init__(self, sll, mobject: Mobject, parent_mobject: Mobject, run_time: float = 1):
        super().__init__(sll, run_time=run_time)
        self._mobject: Mobject = mobject
        self._parent_mobject: Mobject = parent_mobject

    def begin(self):
        self._sll.add(self._mobject)

    def interpolate(self, alpha: float):
        self._mobject.set_opacity(1 - alpha)

    def clean_up_from_animation(self):
        self._sll.remove(self._mobject)
        self._parent_mobject.remove(self._mobject)
        self._mobject.save_state()
        super().clean_up_from_animation()

    def create_successive_counterpart(self) -> LeafSubanimation:
        return FadeOutMobject(self._sll, self._mobject, self._parent_mobject, run_time=self._run_time)
