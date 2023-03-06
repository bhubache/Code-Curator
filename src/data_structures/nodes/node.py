from manim import VMobject, FadeOut, FadeIn, Animation

class Node(VMobject):
    def __init__(self, shape, data):
        super().__init__(color='#DBC9B8')
        self.is_visible = True
        self._radius = 0.5
        self._stroke_width = 2
        self._shape = shape
        self._data = data
        self._container = self._shape(radius=self._radius, stroke_width=self._stroke_width, color=self.color)
        self._container._is_visible = True
        self._container.add(self._data)
        self.add(self._container)
        # self.add(self._data)

    @property
    def data(self):
        return self._data

    def get_visible_components(self):
        visible_components = []
        if self._container._is_visible:
            visible_components.append(self._container)
        
        return visible_components

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

    def animate_fade_out_container(self) -> Animation:
        self._container._is_visible = False
        return FadeOut(self._container)

    def animate_fade_in_container(self) -> Animation:
        self.add(self._container)
        self._container._is_visible = True
        return FadeIn(self._container)

    def fade_out_container(self) -> None:
        self._container._is_visible = False
        FadeOut(self._container)

    def fade_in_container(self) -> None:
        self._container._is_visible = True
        FadeIn(self._container)

    @property
    def container(self):
        return self._container