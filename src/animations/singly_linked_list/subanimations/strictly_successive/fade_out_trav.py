from ..base_subanimation import BaseSubanimation
from manim import Scene

class SuccessiveFadeOutTrav(BaseSubanimation):
    def __init__(self, sll, trav):
        super().__init__(sll)
        self._trav = trav
    
    def begin(self):
        super().begin()

    def interpolate(self, alpha: float):
        self._trav.set_opacity(1 - alpha)
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.remove(self._trav)
        self._sll.save_state()