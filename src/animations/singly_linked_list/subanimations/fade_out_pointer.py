from .visible_subanimation import VisibleSubanimation
from manim import Scene

class FadeOutPointer(VisibleSubanimation):
    def __init__(self, sll, pointer):
        super().__init__(sll)
        self._pointer = pointer
    
    def begin(self):
        super().begin()
        self._pointer.set_opacity(0)

    def interpolate(self, alpha: float):
        self._pointer.set_opacity(alpha)
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.remove(self._pointer)
        self._sll.save_state()

    # TODO: Check if pointer needs to be removed from scene