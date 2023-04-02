from .leaf_subanimation import LeafSubanimation
from manim import Scene, Mobject

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class FadeInContainer(LeafSubanimation):
    def __init__(self, sll, container, node) -> None:
        super().__init__(sll)
        self._container = container
        self._node = node
        self._set_container_opacity(0)

    def begin(self) -> None:
        # self._node.add(self._container)
        # self._sll.add(self._node)
        self._node.add(self._container)


        self._sll.add(self._container)

    def interpolate(self, alpha: float) -> None:
        self._set_container_opacity(alpha)

    def clean_up_from_animation(self) -> None:
        # self._sll.remove(self._container)
        super().clean_up_from_animation()

    def _set_container_opacity(self, opacity: float) -> float:
        self._container.set_stroke(opacity=opacity)
        for submobject in self._container.submobjects:
            submobject.set_opacity(opacity)

    def create_successive_counterpart(self) -> LeafSubanimation:
        return FadeInContainer(self._sll, self._container, self._node)
