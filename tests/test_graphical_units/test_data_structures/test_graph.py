from __future__ import annotations

from typing import Any

import pytest
from manim import BLUE
from manim import ORIGIN
from manim import Scene
from manim import Square
from manim import WHITE
from manim.utils.testing.frames_comparison import frames_comparison

from code_curator.data_structures.graph import Vertex


__module_test__ = "data_structures"


@pytest.fixture
def default_vertex_kwargs() -> dict[str, Any]:
    return dict(  # noqa: C408
        label=0,
        contents=None,
        contents_font_size=15,
        position_relative_to=ORIGIN,
        color=WHITE,
        container=None,
        container_stroke_width=0.75,
        radius=0.2,
        position=(0.0, 0.0, 0.0),
        label_out=False,
        label_dist=0.0,
        label_revolve_angle_in_degrees=0.0,
        label_rotate_angle_in_degrees=0.0,
        show_label=True,
        show_container=True,
    )


@frames_comparison
@pytest.mark.parametrize(
    "kwargs_to_change",
    (
        {},
        {"position": (0.0, -2.0, 0.0)},
        {"show_label": False},
        {"color": BLUE},
        {"container": Square()},
        {"container_stroke_width": 5.0},
        {"radius": 1.0},
        {"label_out": True},
        {"label_dist": 0.2},
        {"label_revolve_angle_in_degrees": 90.0},
        {"label_rotate_angle_in_degrees": 90.0},
        {"show_container": False},
        {"position_relative_to": (0.0, -2.0, 0.0)},
        {"contents": 5, "label_out": True},
        {"contents": 5, "show_label": False},
        {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 90},
        {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 45},
        {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 90, "label_dist": 1},
        {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 45, "label_dist": 1},
        {"position": (2.0, 0.0, 0.0), "position_relative_to": (-0.5, 1.0, 0.0)},
        {"position": (2.0, 0.0, 0.0), "position_relative_to": Vertex(label=0, position=(-0.5, 1.0, 0.0))},
        {
            "contents": 5,
            "label_out": True,
            "label_revolve_angle_in_degrees": 45,
            "position": (2.0, 0.0, 0.0),
            "position_relative_to": (-0.5, 1.0, 0.0),
        },
        {
            "contents": 5,
            "label_out": True,
            "label_revolve_angle_in_degrees": 45,
            "label_dist": 1,
            "position": (2.0, 0.0, 0.0),
            "position_relative_to": (-0.5, 1.0, 0.0),
        },
        {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 45, "radius": 1},
        {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 45, "label_dist": 1, "radius": 1},
        {"position": (2.0, 0.0, 0.0), "position_relative_to": (-0.5, 1.0, 0.0), "radius": 1},
        {"position": (2.0, 0.0, 0.0), "position_relative_to": Vertex(label=0, position=(-0.5, 1.0, 0.0)), "radius": 1},
        {
            "contents": 5,
            "label_out": True,
            "label_revolve_angle_in_degrees": 45,
            "position": (2.0, 0.0, 0.0),
            "position_relative_to": (-0.5, 1.0, 0.0),
            "radius": 1,
        },
        {
            "contents": 5,
            "label_out": True,
            "label_revolve_angle_in_degrees": 45,
            "label_dist": 1,
            "position": (2.0, 0.0, 0.0),
            "position_relative_to": (-0.5, 1.0, 0.0),
            "radius": 1,
        },
    ),
)
def test_vertex(scene: Scene, default_vertex_kwargs, kwargs_to_change) -> None:
    default_vertex_kwargs.update(kwargs_to_change)
    scene.add(
        Vertex(
            **default_vertex_kwargs,
        ),
    )
