from ..base_subanimation import BaseSubanimation
from manim import Scene

class SuccessiveFadeInNode(BaseSubanimation):
    def __init__(self, sll, node):
        super().__init__(sll)
        self._node = node

    def begin(self):
        self._sll.add(self._node)
        container = self._node.container
        container.set_stroke(opacity=0)
        for submobject in container.submobjects:
            submobject.set_opacity(0)

    def interpolate(self, alpha: float):
        container = self._node.container
        container.set_stroke(opacity=alpha)
        for submobject in container.submobjects:
            submobject.set_opacity(alpha)
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.add(self._node)
        # self._save_sll_state()
        self._sll.save_state()