from manim import CurvedArrow

from .edge import Edge

class SinglyDirectedEdge(Edge):
    def __init__(self, start = None, end = None, weight = None, tip_shape = None):
        super().__init__(start=start, end=end, weight=weight)
        self._add_tip(tip_shape=tip_shape, tip_length=0.2, tip_width=0.2)

    def _add_tip(self, tip_shape, tip_length, tip_width) -> None:
        self._line.add_tip(tip_shape=tip_shape, tip_length=tip_length, tip_width=tip_width)

    def create_curved_pointer(start: list[float, float, float], end: list[float, float, float], **kwargs):
        singly_directed_edge = SinglyDirectedEdge(0, 1)
        curved_pointer = CurvedArrow(
            start,
            end,
            tip_length=singly_directed_edge.tip.length,
            **kwargs)
        curved_pointer.set_color('#DBC9B8')
        curved_pointer.set_stroke_width(singly_directed_edge.stroke_width)


        return curved_pointer
