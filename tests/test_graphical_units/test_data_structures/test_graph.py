from __future__ import annotations

from typing import Any
from typing import TYPE_CHECKING

import pytest
from manim import BLUE
from manim import Circle
from manim import Dot
from manim import DOWN
from manim import LEFT
from manim import Mobject
from manim import ORIGIN
from manim import RED
from manim import RIGHT
from manim import Scene
from manim import Square
from manim import UP
from manim import WHITE

from code_curator.data_structures.graph import Edge
from code_curator.data_structures.graph import LabeledLine
from code_curator.data_structures.graph import Vertex
from code_curator.utils.testing.curator_frames_comparison import curator_frames_comparison

if TYPE_CHECKING:
    from code_curator.base_scene import BaseScene


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


@curator_frames_comparison
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
class test_vertex:
    def __init__(self, scene: BaseScene, default_vertex_kwargs, kwargs_to_change) -> None:
        self.scene = scene
        self.vertex_kwargs = default_vertex_kwargs | kwargs_to_change

    def test_vertex(self):
        self.scene.add(
            Vertex(
                **self.vertex_kwargs,
            ),
        )


@curator_frames_comparison(last_frame=False)
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
class test_vertex_movement:
    def __init__(self, scene: Scene, default_vertex_kwargs: dict[str, Any], kwargs_to_change: dict[str, Any]) -> None:
        self.scene = scene
        self.vertex_kwargs = default_vertex_kwargs | kwargs_to_change

    def move_vertex(self):
        new_loc = (-1.0, 0.0, 0.0)
        dot = Dot(new_loc, color=RED)
        self.scene.add_foreground_mobject(dot)

        vertex = Vertex(**self.vertex_kwargs)
        self.scene.add(vertex)
        return vertex.animate.move_to(new_loc)


@pytest.fixture
def default_edge_kwargs(default_vertex_kwargs: dict[str, Any]) -> dict[str, Any]:
    vertex_one_kwargs = default_vertex_kwargs | {
        "label": 1,
        "position": (-1, 0, 0),
    }

    vertex_two_kwargs = default_vertex_kwargs | {
        "label": 2,
        "position": (1, 0, 0),
    }

    return dict(  # noqa: C408
        vertex_one_kwargs=vertex_one_kwargs,
        vertex_two_kwargs=vertex_two_kwargs,
        label=None,
        color=WHITE,
        opacity=1,
        line_stroke_width=0.75,
        label_distance_proportion=0.5,
        label_line_sep=0.1,
        label_container=None,
        label_out=False,
        label_revolve_angle_in_degrees=0,
        label_rotate_angle_in_degrees=0,
        tip_length=0.1,
        tip_width=0.075,
        directedness="-",
    )


@curator_frames_comparison
@pytest.mark.parametrize(
    "kwargs_to_change",
    (
        {},
        {"color": BLUE},
        {"line_stroke_width": 5.0},
        {"tip_length": 1},
        {"tip_width": 0.5},
        {"directedness": "->"},
        {"directedness": "<-"},
        pytest.param({"directedness": "<->"}, marks=pytest.mark.skip(reason="CUR-15")),
        {"directedness": "->", "tip_length": 1},
        {"directedness": "->", "tip_width": 0.5},
        {"directedness": "->", "tip_length": 1, "tip_width": 0.5},
        {"directedness": "<-", "tip_length": 1},
        {"directedness": "<-", "tip_width": 0.5},
        {"directedness": "<-", "tip_length": 1, "tip_width": 0.5},
        pytest.param({"directedness": "<->", "tip_length": 0.25}, marks=pytest.mark.skip(reason="CUR-15")),
        pytest.param({"directedness": "<->", "tip_width": 0.5}, marks=pytest.mark.skip(reason="CUR-15")),
        pytest.param(
            {"directedness": "<->", "tip_length": 0.25, "tip_width": 0.5},
            marks=pytest.mark.skip(reason="CUR-15"),
        ),
        {"vertex_one_kwargs": {"position": (-1.0, -1.0, 0.0)}},
    ),
)
class test_edge:
    def __init__(self, scene: BaseScene, default_edge_kwargs: dict[str, Any], kwargs_to_change: dict[str, Any]) -> None:
        self.scene = scene
        vertex_one_default_kwargs = default_edge_kwargs.pop("vertex_one_kwargs")
        default_edge_kwargs["vertex_one"] = Vertex(
            **(vertex_one_default_kwargs | kwargs_to_change.pop("vertex_one_kwargs", {})),
        )

        vertex_two_default_kwargs = default_edge_kwargs.pop("vertex_two_kwargs")
        default_edge_kwargs["vertex_two"] = Vertex(
            **(vertex_two_default_kwargs | kwargs_to_change.pop("vertex_two_kwargs", {})),
        )

        scene.add(default_edge_kwargs["vertex_one"])
        scene.add(default_edge_kwargs["vertex_two"])

        default_edge_kwargs.update(kwargs_to_change)
        self.edge_kwargs = default_edge_kwargs

    def method(self):
        self.scene.add(Edge(**self.edge_kwargs))


@curator_frames_comparison(last_frame=False)
@pytest.mark.parametrize(
    "kwargs_to_change",
    (
        # Undirected edge
        {},
        {"new_vertex_one_loc": (-2.0, 0.0, 0.0)},
        {"new_vertex_one_loc": (-2.0, -1.0, 0.0)},
        {"new_vertex_two_loc": (2.0, 0.0, 0.0)},
        {"new_vertex_two_loc": (2.0, -1.0, 0.0)},
        {"new_vertex_one_loc": (-2.0, 0.0, 0.0), "new_vertex_two_loc": (2.0, -1.0, 0.0)},
        {"new_vertex_one_loc": (2.0, 0.0, 0.0)},
        {"new_vertex_one_loc": (1.0, 0.0, 0.0), "new_vertex_two_loc": (-1.0, 0.0, 0.0)},
        {"new_vertex_one_loc": (1.5, -0.25, 0.0)},
        # Right directed edge
        {"new_vertex_one_loc": (-2.0, 0.0, 0.0), "directedness": "->"},
        {"new_vertex_two_loc": (2.0, 0.0, 0.0), "directedness": "->"},
        {"new_vertex_two_loc": (2.0, -1.0, 0.0), "directedness": "->"},
        {"new_vertex_one_loc": (-2.0, 0.0, 0.0), "new_vertex_two_loc": (2.0, -1.0, 0.0), "directedness": "->"},
        {"new_vertex_one_loc": (2.0, 0.0, 0.0), "directedness": "->"},
        {"new_vertex_one_loc": (1.0, 0.0, 0.0), "new_vertex_two_loc": (-1.0, 0.0, 0.0), "directedness": "->"},
        {"new_vertex_one_loc": (1.5, -0.25, 0.0), "directedness": "->"},
        # Left directed edge
        {"new_vertex_one_loc": (-2.0, 0.0, 0.0), "directedness": "<-"},
        {"new_vertex_two_loc": (2.0, 0.0, 0.0), "directedness": "<-"},
        {"new_vertex_two_loc": (2.0, -1.0, 0.0), "directedness": "<-"},
        {"new_vertex_one_loc": (-2.0, 0.0, 0.0), "new_vertex_two_loc": (2.0, -1.0, 0.0), "directedness": "<-"},
        {"new_vertex_one_loc": (2.0, 0.0, 0.0), "directedness": "<-"},
        {"new_vertex_one_loc": (1.0, 0.0, 0.0), "new_vertex_two_loc": (-1.0, 0.0, 0.0), "directedness": "<-"},
        {"new_vertex_one_loc": (1.5, -0.25, 0.0), "directedness": "<-"},
        # Double directed edge
        pytest.param(
            {"new_vertex_one_loc": (-2.0, 0.0, 0.0), "directedness": "<->"},
            marks=pytest.mark.skip(reason="FIXME CUR-15: Fix double headed arrow sizes"),
        ),
        pytest.param(
            {"new_vertex_two_loc": (2.0, 0.0, 0.0), "directedness": "<->"},
            marks=pytest.mark.skip(reason="FIXME CUR-15: Fix double headed arrow sizes"),
        ),
        pytest.param(
            {"new_vertex_two_loc": (2.0, -1.0, 0.0), "directedness": "<->"},
            marks=pytest.mark.skip(reason="FIXME CUR-15: Fix double headed arrow sizes"),
        ),
        pytest.param(
            {"new_vertex_one_loc": (-2.0, 0.0, 0.0), "new_vertex_two_loc": (2.0, -1.0, 0.0), "directedness": "<->"},
            marks=pytest.mark.skip(reason="FIXME CUR-15: Fix double headed arrow sizes"),
        ),
        pytest.param(
            {"new_vertex_one_loc": (2.0, 0.0, 0.0), "directedness": "<->"},
            marks=pytest.mark.skip(reason="FIXME CUR-16: Arrow head disappears"),
        ),
        pytest.param(
            {"new_vertex_one_loc": (1.0, 0.0, 0.0), "new_vertex_two_loc": (-1.0, 0.0, 0.0), "directedness": "<->"},
            marks=pytest.mark.skip(reason="FIXME CUR-15: Fix double headed arrow sizes"),
        ),
        pytest.param(
            {"new_vertex_one_loc": (1.5, -0.25, 0.0), "directedness": "<->"},
            marks=pytest.mark.skip(reason="FIXME CUR-16: Arrow head disappears"),
        ),
    ),
)
class test_edge_movement:
    def __init__(self, scene: BaseScene, default_edge_kwargs: dict[str, Any], kwargs_to_change: dict[str, Any]) -> None:
        vertex_one_default_kwargs = default_edge_kwargs.pop("vertex_one_kwargs")
        default_edge_kwargs["vertex_one"] = Vertex(
            **(vertex_one_default_kwargs | kwargs_to_change.pop("vertex_one_kwargs", {})),
        )

        vertex_two_default_kwargs = default_edge_kwargs.pop("vertex_two_kwargs")
        default_edge_kwargs["vertex_two"] = Vertex(
            **(vertex_two_default_kwargs | kwargs_to_change.pop("vertex_two_kwargs", {})),
        )

        scene.add(default_edge_kwargs["vertex_one"])
        scene.add(default_edge_kwargs["vertex_two"])

        new_vertex_one_loc = kwargs_to_change.pop("new_vertex_one_loc", default_edge_kwargs["vertex_one"].get_center())
        new_vertex_two_loc = kwargs_to_change.pop("new_vertex_two_loc", default_edge_kwargs["vertex_two"].get_center())

        default_edge_kwargs.update(kwargs_to_change)
        scene.add(Edge(**default_edge_kwargs))

        self.vertex_one = default_edge_kwargs["vertex_one"]
        self.vertex_two = default_edge_kwargs["vertex_two"]
        self.vertex_one_location = new_vertex_one_loc
        self.vertex_two_location = new_vertex_two_loc

    def animation(self):
        return self.vertex_one.animate.move_to(self.vertex_one_location), self.vertex_two.animate.move_to(
            self.vertex_two_location,
        )


@pytest.fixture
def default_labeled_line_kwargs() -> dict[str, Any]:
    return dict(  # noqa: C408
        start=(0.0, 1.0, 0.0),
        end=(0.0, 0.0, 0.0),
        direction=None,
        label_font_size=15,
        length=0.75,
        label="",
        label_dist=0.1,
        color=WHITE,
        label_color=WHITE,
        tip_length=0.1,
        tip_width=0.075,
        directedness="->",
    )


@curator_frames_comparison
@pytest.mark.parametrize(
    "kwargs_to_change",
    (
        {},
        {"start": (0.0, 3.0, 0.0), "end": (0.0, -2.0, 0.0)},
        {"label": "pointer"},
        {"label": "pointer", "label_dist": 0.5},
        {"color": BLUE},
        {"label": "pointer", "color": BLUE},
        {"tip_length": 0.5},
        {"tip_width": 0.5},
        {"tip_length": 0.5, "tip_width": 0.5},
        {"start": Vertex(0, color=WHITE), "end": None, "direction": DOWN},
        {"start": Vertex(0, color=WHITE), "end": None, "direction": DOWN, "label": "pointer"},
        {"start": Vertex(0, color=WHITE), "end": None, "direction": UP, "label": "pointer"},
        {"start": Vertex(0, color=WHITE), "end": None, "direction": LEFT, "label": "pointer", "label_dist": 0.5},
        {"start": Vertex(0, color=WHITE), "end": None, "direction": RIGHT, "label": "pointer", "label_dist": 0.5},
        {"start": (-1.0, 1.0, 0.0), "end": Vertex(0, color=WHITE), "label": "pointer"},
        {"start": (-1.0, 1.0, 0.0), "end": Vertex(0, color=WHITE), "label": "pointer", "length": 2.0},
        pytest.param(
            {"end": (-1.0, 1.0, 0.0), "start": Vertex(0, color=WHITE), "label": "pointer", "length": 2.0},
            marks=pytest.mark.skip(reason="TODO CUR-17"),
        ),
    ),
)
class test_labeled_line:
    def __init__(
        self,
        scene: BaseScene,
        default_labeled_line_kwargs: dict[str, Any],
        kwargs_to_change: dict[str, Any],
    ) -> None:
        self.scene = scene

        default_labeled_line_kwargs.update(kwargs_to_change)
        if isinstance(default_labeled_line_kwargs.get("start", None), Mobject):
            scene.add(default_labeled_line_kwargs["start"])

        if isinstance(default_labeled_line_kwargs.get("end", None), Mobject):
            scene.add(default_labeled_line_kwargs["end"])

        self.labeled_line_kwargs = default_labeled_line_kwargs

    def method(self):
        self.scene.add(LabeledLine(**self.labeled_line_kwargs))


@curator_frames_comparison(last_frame=False)
@pytest.mark.parametrize(
    "kwargs_to_change",
    (
        {"start": Vertex(0, color=WHITE), "end": None, "direction": DOWN},
        {"start": Vertex(0, color=WHITE), "end": None, "direction": DOWN, "label": "pointer"},
        {"start": Vertex(0, color=WHITE), "end": None, "direction": UP, "label": "pointer"},
        {"start": Vertex(0, color=WHITE), "end": None, "direction": LEFT, "label": "pointer", "label_dist": 0.5},
        {"start": Vertex(0, color=WHITE), "end": None, "direction": RIGHT, "label": "pointer", "label_dist": 0.5},
        {"start": (-1.0, 1.0, 0.0), "end": Vertex(0, color=WHITE), "label": "pointer"},
        {"start": (-1.0, 1.0, 0.0), "end": Vertex(0, color=WHITE), "label": "pointer", "length": 2.0},
    ),
)
class test_labeled_line_movement:
    def __init__(
        self,
        scene: BaseScene,
        default_labeled_line_kwargs: dict[str, Any],
        kwargs_to_change: dict[str, Any],
    ) -> None:
        self.scene = scene

        default_labeled_line_kwargs.update(kwargs_to_change)
        if isinstance(default_labeled_line_kwargs.get("start", None), Mobject):
            scene.add(default_labeled_line_kwargs["start"])

        if isinstance(default_labeled_line_kwargs.get("end", None), Mobject):
            scene.add(default_labeled_line_kwargs["end"])

        self.labeled_line = LabeledLine(**default_labeled_line_kwargs)
        scene.add(self.labeled_line)

    def animation(self):
        return self.labeled_line.pointee.animate.move_to((2, 2, 0))


@curator_frames_comparison(last_frame=False)
class test_labeled_line_tip_moves_when_pointee_changes_size:
    def __init__(self, scene: BaseScene, default_labeled_line_kwargs: dict[str, Any]) -> None:
        self.scene = scene
        self.labeled_line_kwargs = default_labeled_line_kwargs

        self.labeled_line_kwargs["start"] = Circle(radius=0.5)
        self.labeled_line_kwargs["end"] = None
        self.labeled_line_kwargs["direction"] = DOWN

    def animation(self):
        self.scene.add(self.labeled_line_kwargs["start"])
        labeled_line = LabeledLine(
            **self.labeled_line_kwargs,
        )
        self.scene.add(labeled_line)

        return labeled_line.pointee.animate.scale(3)
