from ..base_subanimation import BaseSubanimation
from manim import Scene

class SuccessiveFadeInPointer(BaseSubanimation):
    def __init__(self, sll, pointer):
        super().__init__(sll)
        self._pointer = pointer
    
    def begin(self):
        self._sll.add(self._pointer)
        self._pointer.set_opacity(0)

    def interpolate(self, alpha: float):
        self._pointer.set_opacity(alpha)
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.add(self._pointer)
        # self._save_sll_state()
        self._sll.save_state()