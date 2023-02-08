from manim import VMobject

class Node(VMobject):
    def __init__(self, shape, data):
        super().__init__(color = '#DBC9B8')
        self._shape = shape
        self._data = data

    @property
    def data(self):
        return self._data