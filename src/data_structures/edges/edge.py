from manim import Line, FadeIn, FadeOut

class Edge(Line):
    def __init__(self, start = None, end = None, weight = None):
        super().__init__(start=start, end=end, color='#DBC9B8', stroke_width=2)
        self._weight = weight

    # FIXME: This is just for vertical edges
    @property
    def vertical_length(self):
        return abs(self.start[1] - self.end[1])

    @property
    def horizontal_length(self):
        return abs(self.start[0] - self.end[0])

    @property
    def length(self):
        return self.get_length()
        # raise NotImplementedError()

    # def fade_out(self):
    #     FadeOut(self)

    # def fade_in(self):
    #     FadeIn(self)

    # def animate_fade_out(self):
    #     return FadeOut(self)

    # def animate_fade_in(self):
    #     return FadeIn(self)
