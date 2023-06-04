from __future__ import annotations


from .value import Value


class Element(Value):
    """
    Tex mobject for a cell's element
    """

    def __init__(self, element):
        super().__init__(element)
        self.font_size = 25
