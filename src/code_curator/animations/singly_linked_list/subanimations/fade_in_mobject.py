from __future__ import annotations

from custom_logging.custom_logger import CustomLogger
from manim import Mobject

from .leaf_subanimation import LeafSubanimation
logger = CustomLogger.getLogger(__name__)

# TODO: Add parent mobject member variable


class FadeInMobject(LeafSubanimation):
    def __init__(self, sll, mobject: Mobject, parent_mobject: Mobject) -> None:
        super().__init__(sll)
        self._mobject: Mobject = mobject
        self._parent_mobject: Mobject = parent_mobject
        self._mobject.set_opacity(0)

    def begin(self) -> None:
        # self._parent_mobject.add(self._mobject)
        # if self._parent_mobject is not self._sll:
        #     self._sll.add(self._parent_mobject)
        self._sll.add(self._mobject)

    def interpolate(self, alpha: float) -> None:
        self._mobject.set_opacity(alpha)

    def clean_up_from_animation(self) -> None:
        # self._sll.remove(self._mobject)
        # self._parent_mobject.add(self._mobject)
        super().clean_up_from_animation()

    def create_successive_counterpart(self) -> LeafSubanimation:
        return FadeInMobject(self._sll, self._mobject, self._parent_mobject)
