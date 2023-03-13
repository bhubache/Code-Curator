from .visible_subanimation import VisibleSubanimation
from manim import Scene

class FadeOutNode(VisibleSubanimation):
    def __init__(self, sll, node):
        super().__init__(sll)
        self._node = node
        self._container = self._node.container

    def begin(self):
        super().begin()
        # container = self._node.container
        # container.set_stroke(opacity=1)
        # for submobject in container.submobjects:
        #     submobject.set_opacity(0)

    def interpolate(self, alpha: float):
        self._container.set_stroke(opacity=1 - alpha)
        for submobject in self._container.submobjects:
            submobject.set_opacity(1 - alpha)
        super().interpolate(alpha)

    def clean_up_from_animation(self):
        self._sll.remove(self._container)
        self._sll.save_state()

    # TODO: Check if node needs to be removed from scene