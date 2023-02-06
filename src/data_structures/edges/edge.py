from manim import Line

class Edge(Line):
    def __init__(self, start = None, end = None, weight = None):
        super().__init__(start=start, end=end, color='#DBC9B8', stroke_width=2)
        self._weight = weight
