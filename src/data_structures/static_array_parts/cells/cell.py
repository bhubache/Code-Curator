from manim import *

from ..values.value import Value

class Cell(Rectangle):
    def __init__(self, value, width = 1, height = 1, stroke_width = 2):
        super().__init__(color = '#DBC9B8', width=width, height=height, stroke_width=stroke_width)

        # This if statement is to create values for the descriptor cells
        if isinstance(value, str):
            value = Value(value)
        self._value = value
        
        self._value.move_to(self.get_center())
        self._value.shift(UP * 0.15)
        self.add(self._value)