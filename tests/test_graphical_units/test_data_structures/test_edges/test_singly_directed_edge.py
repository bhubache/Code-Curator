from __future__ import annotations

from data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from manim import Animation
from manim import Scene
from manim.utils.testing.frames_comparison import frames_comparison

__module_test__ = 'edges'


@frames_comparison(last_frame=False)
def test_singly_directed_edge(scene: Scene) -> None:
    singly_directed_edge: SinglyDirectedEdge = SinglyDirectedEdge()
    scene.play(Animation(singly_directed_edge))
