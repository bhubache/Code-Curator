from .visible_subanimation import VisibleSubanimation
from .strictly_successive.fade_out_trav import SuccessiveFadeOutTrav
from manim import Scene

class FadeOutTrav(VisibleSubanimation):
    def __init__(self, sll, trav):
        super().__init__(sll)
        self._trav = trav

    def create_successive_counterpart(self):
        return SuccessiveFadeOutTrav(self._sll, self._trav)

    def interpolate(self, alpha: float):
        self._trav.set_opacity(1 - alpha)
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.remove(self._trav)
        self._sll.save_state()