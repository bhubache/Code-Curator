from __future__ import annotations

from custom_logging.custom_logger import CustomLogger

from .leaf_subanimation import LeafSubanimation
logger = CustomLogger.getLogger(__name__)


class FadeOutContainer(LeafSubanimation):
    def __init__(self, sll, container, node) -> None:
        super().__init__(sll)
        self._container = container
        self._node = node

    def begin(self) -> None:
        pass
        # self._sll.add(self._container)
        # self._set_container_opacity(0)

    def interpolate(self, alpha: float) -> None:
        self._set_container_opacity(1 - alpha)

    def clean_up_from_animation(self) -> None:
        self._node.remove(self._container)
        super().clean_up_from_animation()

    def _set_container_opacity(self, opacity: float) -> float:
        self._container.set_stroke(opacity=opacity)
        for submobject in self._container.submobjects:
            submobject.set_opacity(opacity)

    def create_successive_counterpart(self) -> LeafSubanimation:
        return FadeOutContainer(self._sll, self._container, self._node)
