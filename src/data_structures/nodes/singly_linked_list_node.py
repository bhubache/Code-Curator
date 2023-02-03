from manim import *

from .linear_node import LinearNode
from data_structures.static_array_parts.values.element import Element

class SLLNode(LinearNode):
    def __init__(self, data, shape = Circle):
        super().__init__(shape, Element(data))
        self.add(self._shape(radius=0.5, stroke_width=2, color=self.color))
        self.add(self.data)