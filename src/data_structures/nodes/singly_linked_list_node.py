from __future__ import annotations

from manim import Circle

from .linear_node import LinearNode
from src.custom_logging.custom_logger import CustomLogger
from src.custom_vmobject import CustomVMobject
logger = CustomLogger.getLogger(__name__)


class SLLNode(LinearNode):
    def __init__(self, data: float | str, shape: CustomVMobject | None = None):
        if shape is None:
            shape = Circle
        super().__init__(data, shape)

    @property
    def radius(self):
        return self._radius
