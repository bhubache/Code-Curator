from .base_subanimation import BaseSubanimation
from manim import Scene, Mobject

class FadeInMobject(BaseSubanimation):
    def __init__(self, sll, mobject: Mobject):
        super().__init__(sll)
        self._mobject: Mobject = mobject

    def create_successive_counterpart(self):
        return FadeInMobject(self._sll, self._mobject)
    
    def begin(self):
        self._sll.add(self._mobject)
        self._mobject.set_opacity(0)

    def interpolate(self, alpha: float):
        self._trav.set_opacity(alpha)

    def clean_up_from_animation(self):
        self._mobject.save_state()
        self._sll.save_state()