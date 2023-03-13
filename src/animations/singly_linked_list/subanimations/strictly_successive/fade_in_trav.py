from ..base_subanimation import BaseSubanimation
from manim import Scene

class SuccessiveFadeInTrav(BaseSubanimation):
    def __init__(self, sll, trav):
        super().__init__(sll)
        self._trav = trav
    
    def begin(self):
        self._sll.add(self._trav)
        self._trav.set_opacity(0)

    def interpolate(self, alpha: float):
        self._trav.set_opacity(alpha)
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.add(self._trav)
        self._trav.save_state()
        self._sll.save_state()