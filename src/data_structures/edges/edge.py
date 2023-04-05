from manim import Line, VMobject

class Edge(VMobject):
    def __init__(self, start = None, end = None, weight = None):
        super().__init__()
        self._line: Line = Line(start=start, end=end, color='#DBC9B8', stroke_width=2)
        # super().__init__(start=start, end=end, color='#DBC9B8', stroke_width=2)
        self._weight = weight

        self.add(self._line)

    def get_start_and_end(self):
        return self._line.get_start_and_end()

    # FIXME: This is just for vertical edges
    @property
    def vertical_length(self):
        return abs(self._line.start[1] - self._line.end[1])

    @property
    def horizontal_length(self):
        return abs(self._line.start[0] - self._line.end[0])

    @property
    def length(self):
        return self.get_length()
