# from manim import *

from .edge import Edge

class SinglyDirectedEdge(Edge):
    def __init__(self, start = None, end = None, weight = None, tip_shape = None):
        super().__init__(start=start, end=end, weight=weight)
        self.add_tip(tip_shape=tip_shape, tip_length=0.2, tip_width=0.2)
