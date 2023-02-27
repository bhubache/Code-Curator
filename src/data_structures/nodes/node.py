from manim import VMobject

class Node(VMobject):
    def __init__(self, shape, data):
        super().__init__(color='#DBC9B8')
        self.is_visible = True
        self._radius = 0.5
        self._stroke_width = 2
        self._shape = shape
        self._data = data
        self._container = self._shape(radius=self._radius, stroke_width=self._stroke_width, color=self.color)
        self.add(self._container)
        self.add(self._data)

    @property
    def data(self):
        return self._data

    def get_container_center(self):
        return self._container.get_center()

    def get_container_top(self):
        return self._container.get_top()

    def get_container_right(self):
        return self._container.get_right()

    def get_container_bottom(self):
        return self._container.get_bottom()

    def get_container_left(self):
        return self._container.get_left()