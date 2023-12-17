from __future__ import annotations

from typing import Any

import pytest
from manim import BLUE
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
from manim.utils.testing.frames_comparison import frames_comparison

from code_curator.data_structures.graph import Edge
from code_curator.data_structures.graph import LabeledLine
from code_curator.data_structures.graph import Vertex


__module_test__ = "data_structures"


# @pytest.fixture
# def default_vertex_kwargs() -> dict[str, Any]:
#     return dict(  # noqa: C408
#         label=0,
#         contents=None,
#         contents_font_size=15,
#         position_relative_to=ORIGIN,
#         color=WHITE,
#         container=None,
#         container_stroke_width=0.75,
#         radius=0.2,
#         position=(0.0, 0.0, 0.0),
#         label_out=False,
#         label_dist=0.0,
#         label_revolve_angle_in_degrees=0.0,
#         label_rotate_angle_in_degrees=0.0,
#         show_label=True,
#         show_container=True,
#     )
#
#
# @frames_comparison
# @pytest.mark.parametrize(
#     "kwargs_to_change",
#     (
#         {},
#         {"position": (0.0, -2.0, 0.0)},
#         {"show_label": False},
#         {"color": BLUE},
#         {"container": Square()},
#         {"container_stroke_width": 5.0},
#         {"radius": 1.0},
#         {"label_out": True},
#         {"label_dist": 0.2},
#         {"label_revolve_angle_in_degrees": 90.0},
#         {"label_rotate_angle_in_degrees": 90.0},
#         {"show_container": False},
#         {"position_relative_to": (0.0, -2.0, 0.0)},
#         {"contents": 5, "label_out": True},
#         {"contents": 5, "show_label": False},
#         {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 90},
#         {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 45},
#         {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 90, "label_dist": 1},
#         {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 45, "label_dist": 1},
#         {"position": (2.0, 0.0, 0.0), "position_relative_to": (-0.5, 1.0, 0.0)},
#         {"position": (2.0, 0.0, 0.0), "position_relative_to": Vertex(label=0, position=(-0.5, 1.0, 0.0))},
#         {
#             "contents": 5,
#             "label_out": True,
#             "label_revolve_angle_in_degrees": 45,
#             "position": (2.0, 0.0, 0.0),
#             "position_relative_to": (-0.5, 1.0, 0.0),
#         },
#         {
#             "contents": 5,
#             "label_out": True,
#             "label_revolve_angle_in_degrees": 45,
#             "label_dist": 1,
#             "position": (2.0, 0.0, 0.0),
#             "position_relative_to": (-0.5, 1.0, 0.0),
#         },
#         {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 45, "radius": 1},
#         {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 45, "label_dist": 1, "radius": 1},
#         {"position": (2.0, 0.0, 0.0), "position_relative_to": (-0.5, 1.0, 0.0), "radius": 1},
#         {"position": (2.0, 0.0, 0.0), "position_relative_to": Vertex(label=0, position=(-0.5, 1.0, 0.0)), "radius": 1},
#         {
#             "contents": 5,
#             "label_out": True,
#             "label_revolve_angle_in_degrees": 45,
#             "position": (2.0, 0.0, 0.0),
#             "position_relative_to": (-0.5, 1.0, 0.0),
#             "radius": 1,
#         },
#         {
#             "contents": 5,
#             "label_out": True,
#             "label_revolve_angle_in_degrees": 45,
#             "label_dist": 1,
#             "position": (2.0, 0.0, 0.0),
#             "position_relative_to": (-0.5, 1.0, 0.0),
#             "radius": 1,
#         },
#     ),
# )
# def test_vertex(scene: Scene, default_vertex_kwargs, kwargs_to_change) -> None:
#     default_vertex_kwargs.update(kwargs_to_change)
#     scene.add(
#         Vertex(
#             **default_vertex_kwargs,
#         ),
#     )


from code_curator.base_scene import BaseScene

# TODO: Remove the need to provide ``unique_value_for_caching_control_data``

def curator_frames_comparison(run_time: float | type | None = None, last_frame: bool = True):

    def get_cls(cls):
        breakpoint()
        # Translate class into BaseScene instance that plays the CuratorAnimation
        # Need:
        # 1. The start time of each animation method
        # 2. Total run time
        print(run_time)

        excluded_attr_names = ("pytestmark")
        animation_functions = []

        for attr_name, attr in cls.__dict__.items():
            if attr_name not in excluded_attr_names and not attr_name.startswith("__") and not attr_name.endswith("__"):
                animation_functions.append(attr)

        class AnimationScript:
            def __init__(self) -> None:
                self.entries = []

        animation_script = AnimationScript()
        animation_script.run_time = run_time

        for func in animation_functions:
            try:
                start_time = func.start_time
            except AttributeError:
                start_time = 0.0

            animation_script.entries.append(
                {
                    "name": func.__name__,
                    "start_time": start_time
                }
            )

        base_scene = BaseScene(animation_script)

        for func in animation_functions:
            setattr(type(base_scene), func.__name__, func)

        def test_manim_func_wrapper(scene, *args):
            breakpoint()
            # base_scene.unique_value = unique_value
            # base_scene.sll = sll
            # scene.__dict__.update(base_scene.__dict__)
            from manim import Circle
            from manim import FadeIn
            return lambda : scene.play(FadeIn(Circle()))
            # return BaseScene.construct(scene)
            # return base_scene.construct()

        test_manim_func_wrapper.__dict__["pytestmark"] = cls.__dict__["pytestmark"]

        return frames_comparison(func=test_manim_func_wrapper, last_frame=last_frame)

    if callable(run_time):
        _cls = run_time
        run_time = 1.0
        return get_cls(_cls)

    if run_time is None:
        run_time = 1.0

    return get_cls

def curator_deco(cls):
    breakpoint()
    print('hi')


@frames_comparison(last_frame=False, base_scene=BaseScene)
# @curator_frames_comparison(last_frame=False)
@pytest.mark.parametrize(
    "kwargs_to_change",
    (
        {},
        # {"position": (0.0, -2.0, 0.0)},
        # {"show_label": False},
        # {"color": BLUE},
        # {"container": Square()},
        # {"container_stroke_width": 5.0},
        # {"radius": 1.0},
        # {"label_out": True},
        # {"label_dist": 0.2},
        # {"label_revolve_angle_in_degrees": 90.0},
        # {"label_rotate_angle_in_degrees": 90.0},
        # {"show_container": False},
        # {"position_relative_to": (0.0, -2.0, 0.0)},
        # {"contents": 5, "label_out": True},
        # {"contents": 5, "show_label": False},
        # {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 90},
        # {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 45},
        # {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 90, "label_dist": 1},
        # {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 45, "label_dist": 1},
        # {"position": (2.0, 0.0, 0.0), "position_relative_to": (-0.5, 1.0, 0.0)},
        # {"position": (2.0, 0.0, 0.0), "position_relative_to": Vertex(label=0, position=(-0.5, 1.0, 0.0))},
        # {
        #     "contents": 5,
        #     "label_out": True,
        #     "label_revolve_angle_in_degrees": 45,
        #     "position": (2.0, 0.0, 0.0),
        #     "position_relative_to": (-0.5, 1.0, 0.0),
        # },
        # {
        #     "contents": 5,
        #     "label_out": True,
        #     "label_revolve_angle_in_degrees": 45,
        #     "label_dist": 1,
        #     "position": (2.0, 0.0, 0.0),
        #     "position_relative_to": (-0.5, 1.0, 0.0),
        # },
        # {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 45, "radius": 1},
        # {"contents": 5, "label_out": True, "label_revolve_angle_in_degrees": 45, "label_dist": 1, "radius": 1},
        # {"position": (2.0, 0.0, 0.0), "position_relative_to": (-0.5, 1.0, 0.0), "radius": 1},
        # {"position": (2.0, 0.0, 0.0), "position_relative_to": Vertex(label=0, position=(-0.5, 1.0, 0.0)), "radius": 1},
        # {
        #     "contents": 5,
        #     "label_out": True,
        #     "label_revolve_angle_in_degrees": 45,
        #     "position": (2.0, 0.0, 0.0),
        #     "position_relative_to": (-0.5, 1.0, 0.0),
        #     "radius": 1,
        # },
        # {
        #     "contents": 5,
        #     "label_out": True,
        #     "label_revolve_angle_in_degrees": 45,
        #     "label_dist": 1,
        #     "position": (2.0, 0.0, 0.0),
        #     "position_relative_to": (-0.5, 1.0, 0.0),
        #     "radius": 1,
        # },
    ),
)
# @curator_deco
class test_vertex_movement:
    def __init__(self, scene: Scene, default_vertex_kwargs: dict[str, Any], kwargs_to_change: dict[str, Any]) -> None:
        self.scene = scene
        self.default_vertex_kwargs = default_vertex_kwargs
        self.kwargs_to_change = kwargs_to_change

    def move_vertex(self):
        new_loc = (-1.0, 0.0, 0.0)
        dot = Dot(new_loc, color=RED)
        self.scene.add_foreground_mobject(dot)

        vertex = Vertex(**{**self.default_vertex_kwargs, **self.kwargs_to_change})
        self.scene.add(vertex)
        self.scene.play(vertex.animate.move_to(new_loc))


# def test_vertex_movement(scene: Scene, default_vertex_kwargs: dict[str, Any], kwargs_to_change: dict[str, Any]) -> None:
#     new_loc = (-1.0, 0.0, 0.0)
#     dot = Dot(new_loc, color=RED)
#     scene.add_foreground_mobject(dot)
#
#     vertex = Vertex(**{**default_vertex_kwargs, **kwargs_to_change})
#     scene.add(vertex)
#     scene.play(vertex.animate.move_to(new_loc))


# @pytest.fixture
# def default_edge_kwargs(default_vertex_kwargs: dict[str, Any]) -> dict[str, Any]:
#     vertex_one_kwargs = default_vertex_kwargs | {
#         "label": 1,
#         "position": (-1, 0, 0),
#     }
#
#     vertex_two_kwargs = default_vertex_kwargs | {
#         "label": 2,
#         "position": (1, 0, 0),
#     }
#
#     return dict(  # noqa: C408
#         vertex_one_kwargs=vertex_one_kwargs,
#         vertex_two_kwargs=vertex_two_kwargs,
#         label=None,
#         color=WHITE,
#         opacity=1,
#         line_stroke_width=0.75,
#         label_distance_proportion=0.5,
#         label_line_sep=0.1,
#         label_container=None,
#         label_out=False,
#         label_revolve_angle_in_degrees=0,
#         label_rotate_angle_in_degrees=0,
#         tip_length=0.1,
#         tip_width=0.075,
#         directedness="-",
#     )
#
#
# @frames_comparison
# @pytest.mark.parametrize(
#     "kwargs_to_change",
#     (
#         {},
#         {"color": BLUE},
#         {"line_stroke_width": 5.0},
#         {"tip_length": 1},
#         {"tip_width": 0.5},
#         {"directedness": "->"},
#         {"directedness": "<-"},
#         {"directedness": "<->"},
#         {"directedness": "->", "tip_length": 1},
#         {"directedness": "->", "tip_width": 0.5},
#         {"directedness": "->", "tip_length": 1, "tip_width": 0.5},
#         {"directedness": "<-", "tip_length": 1},
#         {"directedness": "<-", "tip_width": 0.5},
#         {"directedness": "<-", "tip_length": 1, "tip_width": 0.5},
#         {"directedness": "<->", "tip_length": 0.25},
#         {"directedness": "<->", "tip_width": 0.5},
#         {"directedness": "<->", "tip_length": 0.25, "tip_width": 0.5},
#         {"vertex_one_kwargs": {"position": (-1.0, -1.0, 0.0)}},
#     ),
# )
# def test_edge(scene: Scene, default_edge_kwargs, kwargs_to_change) -> None:
#     vertex_one_default_kwargs = default_edge_kwargs.pop("vertex_one_kwargs")
#     default_edge_kwargs["vertex_one"] = Vertex(
#         **(vertex_one_default_kwargs | kwargs_to_change.pop("vertex_one_kwargs", {})),
#     )
#
#     vertex_two_default_kwargs = default_edge_kwargs.pop("vertex_two_kwargs")
#     default_edge_kwargs["vertex_two"] = Vertex(
#         **(vertex_two_default_kwargs | kwargs_to_change.pop("vertex_two_kwargs", {})),
#     )
#
#     scene.add(default_edge_kwargs["vertex_one"])
#     scene.add(default_edge_kwargs["vertex_two"])
#
#     default_edge_kwargs.update(kwargs_to_change)
#     scene.add(Edge(**default_edge_kwargs))
#
#
# @frames_comparison(last_frame=False)
# @pytest.mark.parametrize(
#     "kwargs_to_change",
#     (
#         # Undirected edge
#         {},
#         {"new_vertex_one_loc": (-2.0, 0.0, 0.0)},
#         {"new_vertex_one_loc": (-2.0, -1.0, 0.0)},
#         {"new_vertex_two_loc": (2.0, 0.0, 0.0)},
#         {"new_vertex_two_loc": (2.0, -1.0, 0.0)},
#         {"new_vertex_one_loc": (-2.0, 0.0, 0.0), "new_vertex_two_loc": (2.0, -1.0, 0.0)},
#         {"new_vertex_one_loc": (2.0, 0.0, 0.0)},
#         {"new_vertex_one_loc": (1.0, 0.0, 0.0), "new_vertex_two_loc": (-1.0, 0.0, 0.0)},
#         {"new_vertex_one_loc": (1.5, -0.25, 0.0)},
#         # Right directed edge
#         {"new_vertex_one_loc": (-2.0, 0.0, 0.0), "directedness": "->"},
#         {"new_vertex_two_loc": (2.0, 0.0, 0.0), "directedness": "->"},
#         {"new_vertex_two_loc": (2.0, -1.0, 0.0), "directedness": "->"},
#         {"new_vertex_one_loc": (-2.0, 0.0, 0.0), "new_vertex_two_loc": (2.0, -1.0, 0.0), "directedness": "->"},
#         {"new_vertex_one_loc": (2.0, 0.0, 0.0), "directedness": "->"},
#         {"new_vertex_one_loc": (1.0, 0.0, 0.0), "new_vertex_two_loc": (-1.0, 0.0, 0.0), "directedness": "->"},
#         {"new_vertex_one_loc": (1.5, -0.25, 0.0), "directedness": "->"},
#         # Left directed edge
#         {"new_vertex_one_loc": (-2.0, 0.0, 0.0), "directedness": "<-"},
#         {"new_vertex_two_loc": (2.0, 0.0, 0.0), "directedness": "<-"},
#         {"new_vertex_two_loc": (2.0, -1.0, 0.0), "directedness": "<-"},
#         {"new_vertex_one_loc": (-2.0, 0.0, 0.0), "new_vertex_two_loc": (2.0, -1.0, 0.0), "directedness": "<-"},
#         {"new_vertex_one_loc": (2.0, 0.0, 0.0), "directedness": "<-"},
#         {"new_vertex_one_loc": (1.0, 0.0, 0.0), "new_vertex_two_loc": (-1.0, 0.0, 0.0), "directedness": "<-"},
#         {"new_vertex_one_loc": (1.5, -0.25, 0.0), "directedness": "<-"},
#         # Double directed edge
#         # {"new_vertex_one_loc": (-2.0, 0.0, 0.0), "directedness": "<->"},
#         # {"new_vertex_two_loc": (2.0, 0.0, 0.0), "directedness": "<->"},
#         # {"new_vertex_two_loc": (2.0, -1.0, 0.0), "directedness": "<->"},
#         # {"new_vertex_one_loc": (-2.0, 0.0, 0.0), "new_vertex_two_loc": (2.0, -1.0, 0.0), "directedness": "<->"},
#         # FIXME: Arrow pointing to two disappears after vertices pass through eachother
#         # {"new_vertex_one_loc": (2.0, 0.0, 0.0), "directedness": "<->"},
#         # {"new_vertex_one_loc": (1.0, 0.0, 0.0), "new_vertex_two_loc": (-1.0, 0.0, 0.0), "directedness": "<->"},
#         # FIXME: Arrow pointing to two seems to disappear after vertices pass through eachother
#         # {"new_vertex_one_loc": (1.5, -0.25, 0.0), "directedness": "<->"},
#     ),
# )
# def test_edge_movement(scene: Scene, default_edge_kwargs, kwargs_to_change) -> None:
#     vertex_one_default_kwargs = default_edge_kwargs.pop("vertex_one_kwargs")
#     default_edge_kwargs["vertex_one"] = Vertex(
#         **(vertex_one_default_kwargs | kwargs_to_change.pop("vertex_one_kwargs", {})),
#     )
#
#     vertex_two_default_kwargs = default_edge_kwargs.pop("vertex_two_kwargs")
#     default_edge_kwargs["vertex_two"] = Vertex(
#         **(vertex_two_default_kwargs | kwargs_to_change.pop("vertex_two_kwargs", {})),
#     )
#
#     scene.add(default_edge_kwargs["vertex_one"])
#     scene.add(default_edge_kwargs["vertex_two"])
#
#     new_vertex_one_loc = kwargs_to_change.pop("new_vertex_one_loc", default_edge_kwargs["vertex_one"].get_center())
#     new_vertex_two_loc = kwargs_to_change.pop("new_vertex_two_loc", default_edge_kwargs["vertex_two"].get_center())
#
#     default_edge_kwargs.update(kwargs_to_change)
#     scene.add(Edge(**default_edge_kwargs))
#
#     scene.play(
#         default_edge_kwargs["vertex_one"].animate.move_to(new_vertex_one_loc),
#         default_edge_kwargs["vertex_two"].animate.move_to(new_vertex_two_loc),
#     )
#
#
# @pytest.fixture
# def default_labeled_line_kwargs() -> dict[str, Any]:
#     return dict(
#         start=(0.0, 1.0, 0.0),
#         end=(0.0, 0.0, 0.0),
#         direction=None,
#         label_font_size=15,
#         length=0.75,
#         label="",
#         label_dist=0.1,
#         color=WHITE,
#         label_color=WHITE,
#         tip_length=0.1,
#         tip_width=0.075,
#         directedness="->",
#     )
#
#
# @frames_comparison
# @pytest.mark.parametrize(
#     "kwargs_to_change",
#     (
#         {},
#         {"start": (0.0, 3.0, 0.0), "end": (0.0, -2.0, 0.0)},
#         {"label": "pointer"},
#         {"label": "pointer", "label_dist": 0.5},
#         {"color": BLUE},
#         {"label": "pointer", "color": BLUE},
#         {"tip_length": 0.5},
#         {"tip_width": 0.5},
#         {"tip_length": 0.5, "tip_width": 0.5},
#         {"start": Vertex(0, color=WHITE), "end": None, "direction": DOWN},
#         {"start": Vertex(0, color=WHITE), "end": None, "direction": DOWN, "label": "pointer"},
#         {"start": Vertex(0, color=WHITE), "end": None, "direction": UP, "label": "pointer"},
#         {"start": Vertex(0, color=WHITE), "end": None, "direction": LEFT, "label": "pointer", "label_dist": 0.5},
#         {"start": Vertex(0, color=WHITE), "end": None, "direction": RIGHT, "label": "pointer", "label_dist": 0.5},
#         {"start": (-1.0, 1.0, 0.0), "end": Vertex(0, color=WHITE), "label": "pointer"},
#         {"start": (-1.0, 1.0, 0.0), "end": Vertex(0, color=WHITE), "label": "pointer", "length": 2.0},
#         # These scenarios should be unlikely
#         # {"end": (-1.0, 1.0, 0.0), "start": Vertex(0, color=WHITE), "label": "pointer", "length": 2.0},
#         # {"end": Vertex(1, color=WHITE).move_to((-1.0, 1.0, 0.0)), "start": Vertex(0, color=WHITE), "label": "pointer", "length": 2.0},
#     ),
# )
# def test_labeled_line(
#     scene: Scene,
#     default_labeled_line_kwargs: dict[str, Any],
#     kwargs_to_change: dict[str, Any],
# ) -> None:
#     default_labeled_line_kwargs.update(kwargs_to_change)
#     if isinstance(default_labeled_line_kwargs.get("start", None), Mobject):
#         scene.add(default_labeled_line_kwargs["start"])
#
#     if isinstance(default_labeled_line_kwargs.get("end", None), Mobject):
#         scene.add(default_labeled_line_kwargs["end"])
#
#     scene.add(LabeledLine(**default_labeled_line_kwargs))
#
#
# # TODO: LabeledLine movement and pointee movement!
# # @frames_comparison(last_frame=False)
# # @pytest.mark.parametrize(
# #     "kwargs_to_change",
# #     (
# #         # {},
# #         # {"start": (0.0, 3.0, 0.0), "end": (0.0, -2.0, 0.0)},
# #         # {"label": "pointer"},
# #         # {"label": "pointer", "label_dist": 0.5},
# #         # {"color": BLUE},
# #         # {"label": "pointer", "color": BLUE},
# #         # {"tip_length": 0.5},
# #         # {"tip_width": 0.5},
# #         # {"tip_length": 0.5, "tip_width": 0.5},
# #         # {"start": Vertex(0, color=WHITE), "end": None, "direction": DOWN},
# #         # {"start": Vertex(0, color=WHITE), "end": None, "direction": DOWN, "label": "pointer"},
# #         # {"start": Vertex(0, color=WHITE), "end": None, "direction": UP, "label": "pointer"},
# #         # {"start": Vertex(0, color=WHITE), "end": None, "direction": LEFT, "label": "pointer", "label_dist": 0.5},
# #         # {"start": Vertex(0, color=WHITE), "end": None, "direction": RIGHT, "label": "pointer", "label_dist": 0.5},
# #         # {"start": (-1.0, 1.0, 0.0), "end": Vertex(0, color=WHITE), "label": "pointer"},
# #         # {"start": (-1.0, 1.0, 0.0), "end": Vertex(0, color=WHITE), "label": "pointer", "length": 2.0},
# #
# #         # These scenarios should be unlikely
# #         # {"end": (-1.0, 1.0, 0.0), "start": Vertex(0, color=WHITE), "label": "pointer", "length": 2.0},
# #         # {"end": Vertex(1, color=WHITE).move_to((-1.0, 1.0, 0.0)), "start": Vertex(0, color=WHITE), "label": "pointer", "length": 2.0},
# #     ),
# # )
# # def test_labeled_line_movement(scene: Scene, default_labeled_line_kwargs: dict[str, Any], kwargs_to_change: dict[str, Any]) -> None:
# #     default_labeled_line_kwargs.update(kwargs_to_change)
# #     if isinstance(default_labeled_line_kwargs.get("start", None), Mobject):
# #         scene.add(default_labeled_line_kwargs["start"])
# #
# #     if isinstance(default_labeled_line_kwargs.get("end", None), Mobject):
# #         scene.add(default_labeled_line_kwargs["end"])
# #
# #     labeled_line = LabeledLine(**default_labeled_line_kwargs)
# #     scene.add(labeled_line)
# #
# #     scene.play(
# #         labeled_line.animate.move_to()
# #     )
