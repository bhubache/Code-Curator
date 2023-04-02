from manim import Circle

from .linear_node import LinearNode
from data_structures.static_array_parts.values.element import Element

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class SLLNode(LinearNode):
    def __init__(self, data, shape = None):
        if shape is None: shape = Circle
        super().__init__(shape, Element(data))
        # self.add(self._shape(radius=self._radius, stroke_width=self._stroke_width, color=self.color))
        # self.add(self._shape(radius=0.5, stroke_width=2, color=self.color))
        # self.add(self.data)

    @property
    def radius(self):
        return self._radius
        # return 1.25