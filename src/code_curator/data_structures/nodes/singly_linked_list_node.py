from __future__ import annotations

from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.custom_vmobject import CustomVMobject
from manim import Circle

from .linear_node import LinearNode
logger = CustomLogger.getLogger(__name__)


class SLLNode(LinearNode):
    def __init__(self, data: float | str, shape: CustomVMobject | None = None):
        if shape is None:
            shape = Circle
        super().__init__(data, shape)

    @property
    def radius(self):
        return self._radius
