from __future__ import annotations

from data_structures.edges.edge import Edge
from manim import Animation
from manim import Scene
from manim.utils.testing.frames_comparison import frames_comparison

__module_test__ = 'edges'


@frames_comparison(last_frame=False)
def test_edge(scene: Scene) -> None:
    edge: Edge = Edge()
    scene.play(Animation(edge))
