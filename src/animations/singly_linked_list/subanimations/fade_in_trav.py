from .visible_subanimation import VisibleSubanimation
from .strictly_successive.fade_in_trav import SuccessiveFadeInTrav
from manim import Scene

class FadeInTrav(VisibleSubanimation):
    def __init__(self, sll, trav):
        super().__init__(sll)
        self._trav = trav

    def create_successive_counterpart(self):
        return SuccessiveFadeInTrav(self._sll, self._trav)
    
    def begin(self):
        super().begin()
        self._sll.add(self._trav)
        self._trav.set_opacity(0)

    def interpolate(self, alpha: float):
        self._trav.set_opacity(alpha)
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.add(self._trav)
        self._trav.save_state()
        self._sll.save_state()