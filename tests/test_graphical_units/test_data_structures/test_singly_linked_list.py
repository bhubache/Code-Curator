from __future__ import annotations

from typing import Any

import pytest
from manim import DOWN
from manim import Scene
from manim import WHITE
from manim.typing import Vector
from manim.utils.testing.frames_comparison import frames_comparison
# from code_curator.utils.testing.curator_frames_comparison import curator_frames_comparison

from code_curator.data_structures.singly_linked_list_v2 import SinglyLinkedList


__module_test__ = "data_structures"

from code_curator.base_scene import BaseScene
def curator_frames_comparison(
    run_time: float | type | None = None,
    last_frame: bool = True,
    base_scene: Scene | None = None
):

    def get_cls(cls):
        excluded_attr_names = ("pytestmark")
        animation_functions = []

        breakpoint()

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

        # base_scene = BaseScene(animation_script)
        nonlocal base_scene
        if base_scene is None:
            base_scene = BaseScene

        for func in animation_functions:
            # setattr(type(base_scene), func.__name__, func)
            setattr(base_scene, func.__name__, func)

        # def test_manim_func_wrapper(scene, unique_value, sll):
        def test_manim_func_wrapper(scene, *args, **kwargs):
            scene.animation_script = animation_script
            scene.unique_value = unique_value
            scene.sll = sll
            return base_scene.construct(scene)

        test_manim_func_wrapper.__dict__["pytestmark"] = cls.__dict__["pytestmark"]

        # nonlocal base_scene
        # if base_scene is None:
        #     base_scene = BaseScene

        return frames_comparison(func=test_manim_func_wrapper, last_frame=last_frame, base_scene=BaseScene)

    if callable(run_time):
        _cls = run_time
        run_time = 1.0
        return get_cls(_cls)

    if run_time is None:
        run_time = 1.0

    return get_cls


@frames_comparison
@pytest.mark.parametrize(
    "kwargs",
    (
        {"color": WHITE},
        # Invalid SLL
        # {"color": WHITE, "add_head_pointer": True, "add_tail_pointer": True},
        {"color": WHITE, "add_null": True},
        {"color": WHITE, "add_null": True, "add_head_pointer": True, "add_tail_pointer": True},
        {"values": [0], "color": WHITE},
        {"values": [0], "color": WHITE, "add_null": True},
        {"values": [0], "color": WHITE, "add_head_pointer": True, "add_tail_pointer": True},
        {"values": [0], "color": WHITE, "add_null": True, "add_head_pointer": True, "add_tail_pointer": True},
        {"values": [0, 1], "color": WHITE},
        {"values": [0, 1], "color": WHITE, "add_null": True},
        {"values": [0, 1], "color": WHITE, "add_head_pointer": True, "add_tail_pointer": True},
        {"values": [0, 1], "color": WHITE, "add_null": True, "add_head_pointer": True, "add_tail_pointer": True},
        {"values": [0, 1, 2], "color": WHITE},
        {"values": [0, 1, 2], "color": WHITE, "add_null": True},
        {"values": [0, 1, 2], "color": WHITE, "add_head_pointer": True, "add_tail_pointer": True},
        {"values": [0, 1, 2], "color": WHITE, "add_null": True, "add_head_pointer": True, "add_tail_pointer": True},
    ),
)
def test_sll_building(scene: Scene, kwargs: dict[str, Any]) -> None:
    sll = SinglyLinkedList.create_sll(*kwargs.get("values", []), color=kwargs["color"])

    if kwargs.get("add_null", False):
        sll.add_null()

    if kwargs.get("add_head_pointer", False):
        sll.add_head_pointer()

    if kwargs.get("add_tail_pointer", False):
        sll.add_tail_pointer()

    scene.add(sll)


@curator_frames_comparison(last_frame=False)
@pytest.mark.parametrize(
    ("unique_value", "sll",),
    (
        # (0, SinglyLinkedList.create_sll(color=WHITE)),
        # (2, SinglyLinkedList.create_sll(color=WHITE).add_null()),
        # (3, SinglyLinkedList.create_sll(color=WHITE).add_null().add_head_pointer().add_tail_pointer()),
        # (4, SinglyLinkedList.create_sll(0, color=WHITE)),
        # (5, SinglyLinkedList.create_sll(0, color=WHITE).add_head_pointer().add_tail_pointer()),
        # (6, SinglyLinkedList.create_sll(0, color=WHITE).add_null()),
        # (7, SinglyLinkedList.create_sll(0, color=WHITE).add_null().add_head_pointer().add_tail_pointer()),
        (8, SinglyLinkedList.create_sll(0, 1, color=WHITE)),
        # (9, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_head_pointer().add_tail_pointer()),
        # (10, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null()),
        # (11, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer()),
    )
)
class test_adding_null_node_cls:

    def __init__(self, unique_value, sll) -> None:
        self.sll = sll

    def my_animation(self):
        return self.sll.animate.add_null()


@frames_comparison(
    last_frame=False,
    # base_scene=MockBaseScene.set_run_time(1.0).add_animation_method("add_null_node", start_time=0.0),
)
@pytest.mark.parametrize(
    ("unique_value_for_caching_control_data", "sll"),
    (
        (1, SinglyLinkedList.create_sll(color=WHITE)),
        # (2, SinglyLinkedList.create_sll(color=WHITE).add_null()),
        # (3, SinglyLinkedList.create_sll(color=WHITE).add_null().add_head_pointer().add_tail_pointer()),
        # (4, SinglyLinkedList.create_sll(0, color=WHITE)),
        # (5, SinglyLinkedList.create_sll(0, color=WHITE).add_head_pointer().add_tail_pointer()),
        # (6, SinglyLinkedList.create_sll(0, color=WHITE).add_null()),
        # (7, SinglyLinkedList.create_sll(0, color=WHITE).add_null().add_head_pointer().add_tail_pointer()),
        # (8, SinglyLinkedList.create_sll(0, 1, color=WHITE)),
        # (9, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_head_pointer().add_tail_pointer()),
        # (10, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null()),
        # (11, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer()),
    )
)
def test_adding_null_node(scene: Scene, unique_value_for_caching_control_data: int, sll: SinglyLinkedList) -> None:
    scene.add(sll)

    def add_null_node(self):
        return sll.animate.add_null()

    # scene.register_function(add_null_node)

    scene.play()


# @frames_comparison(base_scene=MockBaseScene)
@frames_comparison
@pytest.mark.parametrize(
    ("unique_value_for_caching_control_data", "sll", "index", "value"),
    (
        # Empty
        (0, SinglyLinkedList.create_sll(color=WHITE), 0, 10),
        (1, SinglyLinkedList.create_sll(color=WHITE).add_null(), 0, 10),
        (2, SinglyLinkedList.create_sll(color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 0, 10),
        # One node
        (3, SinglyLinkedList.create_sll(0, color=WHITE), 0, 10),
        (4, SinglyLinkedList.create_sll(0, color=WHITE).add_null(), 0, 10),
        (5, SinglyLinkedList.create_sll(0, color=WHITE).add_head_pointer().add_tail_pointer(), 0, 10),
        (6, SinglyLinkedList.create_sll(0, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 0, 10),
        (7, SinglyLinkedList.create_sll(0, color=WHITE), 1, 10),
        (8, SinglyLinkedList.create_sll(0, color=WHITE).add_null(), 1, 10),
        (9, SinglyLinkedList.create_sll(0, color=WHITE).add_head_pointer().add_tail_pointer(), 1, 10),
        (10, SinglyLinkedList.create_sll(0, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 1, 10),
        # Two nodes
        (11, SinglyLinkedList.create_sll(0, 1, color=WHITE), 0, 10),
        (12, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null(), 0, 10),
        (13, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_head_pointer().add_tail_pointer(), 0, 10),
        (14, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 0, 10),
        (15, SinglyLinkedList.create_sll(0, 1, color=WHITE), 1, 10),
        (16, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null(), 1, 10),
        (17, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_head_pointer().add_tail_pointer(), 1, 10),
        (18, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 1, 10),
        (19, SinglyLinkedList.create_sll(0, 1, color=WHITE), 2, 10),
        (20, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null(), 2, 10),
        (21, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_head_pointer().add_tail_pointer(), 2, 10),
        (22, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 2, 10),
        # Three nodes
        (23, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE), 0, 10),
        (24, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null(), 0, 10),
        (25, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_head_pointer().add_tail_pointer(), 0, 10),
        (26, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 0, 10),
        (27, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE), 1, 10),
        (28, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null(), 1, 10),
        (29, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_head_pointer().add_tail_pointer(), 1, 10),
        (30, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 1, 10),
        (31, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE), 2, 10),
        (32, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null(), 2, 10),
        (33, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_head_pointer().add_tail_pointer(), 2, 10),
        (34, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 2, 10),
        (35, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE), 3, 10),
        (36, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null(), 3, 10),
        (37, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_head_pointer().add_tail_pointer(), 3, 10),
        (38, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 3, 10),
    ),
)
def test_insert(
    scene: Scene,
    unique_value_for_caching_control_data: int,
    sll: SinglyLinkedList,
    index: int,
    value: Any,
) -> None:
    sll.insert_node(index, value, center=True)

    scene.add(sll)


@frames_comparison(
    last_frame=False,
    # base_scene=MockBaseScene.set_run_time(1.0).add_animation_method("move_head_pointer", start_time=0.0),
)
@pytest.mark.parametrize(
    ("unique_value_for_caching_control_data", "sll", "index", "pointer_direction"),
    (
        (1, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer(), 1, DOWN),
        # (1, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer(), 2, DOWN),
        # (1, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer(), "null", DOWN),
        # (1, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer(), 1, UP),
    ),
)
def test_move_head_pointer(
    scene: Scene,
    unique_value_for_caching_control_data: int,
    sll: SinglyLinkedList,
    index: int,
    pointer_direction: Vector,
) -> None:
    scene.add(sll)

    def move_head_pointer(self):
        if index == "null":
            node = sll.null
        else:
            node = sll.get_node(index)

        return sll.animate.move_labeled_pointer(
            sll.head_pointer,
            node,
            pointer_direction=pointer_direction,
        )

    scene.register_function(move_head_pointer)

    scene.play()


# @frames_comparison(
#     last_frame=False,
#     base_scene=MockBaseScene.set_run_time(1.0)
#     .add_animation_method("insert_node_into_sll", start_time=0.0)
# )
# @pytest.mark.parametrize(
#     ("unique_value_for_caching_control_data", "sll", "index", "value"),
#     (
#         # Empty
#         # (0, SinglyLinkedList.create_sll(color=WHITE), 0, 10),
#         (1, SinglyLinkedList.create_sll(color=WHITE).add_null(), 0, 10),
#         # (2, SinglyLinkedList.create_sll(color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 0, 10),
#         # # One node
#         # (3, SinglyLinkedList.create_sll(0, color=WHITE), 0, 10),
#         # (4, SinglyLinkedList.create_sll(0, color=WHITE).add_null(), 0, 10),
#         # (5, SinglyLinkedList.create_sll(0, color=WHITE).add_head_pointer().add_tail_pointer(), 0, 10),
#         # (6, SinglyLinkedList.create_sll(0, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 0, 10),
#         # (7, SinglyLinkedList.create_sll(0, color=WHITE), 1, 10),
#         # (8, SinglyLinkedList.create_sll(0, color=WHITE).add_null(), 1, 10),
#         # (9, SinglyLinkedList.create_sll(0, color=WHITE).add_head_pointer().add_tail_pointer(), 1, 10),
#         # (10, SinglyLinkedList.create_sll(0, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 1, 10),
#         # # Two nodes
#         # (11, SinglyLinkedList.create_sll(0, 1, color=WHITE), 0, 10),
#         # (12, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null(), 0, 10),
#         # (13, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_head_pointer().add_tail_pointer(), 0, 10),
#         # (14, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 0, 10),
#         # (15, SinglyLinkedList.create_sll(0, 1, color=WHITE), 1, 10),
#         # (16, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null(), 1, 10),
#         # (17, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_head_pointer().add_tail_pointer(), 1, 10),
#         # (18, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 1, 10),
#         # (19, SinglyLinkedList.create_sll(0, 1, color=WHITE), 2, 10),
#         # (20, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null(), 2, 10),
#         # (21, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_head_pointer().add_tail_pointer(), 2, 10),
#         # (22, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 2, 10),
#         # # Three nodes
#         # (23, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE), 0, 10),
#         # (24, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null(), 0, 10),
#         # (25, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_head_pointer().add_tail_pointer(), 0, 10),
#         # (26, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 0, 10),
#         # (27, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE), 1, 10),
#         # (28, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null(), 1, 10),
#         # (29, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_head_pointer().add_tail_pointer(), 1, 10),
#         # (30, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 1, 10),
#         # (31, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE), 2, 10),
#         # (32, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null(), 2, 10),
#         # (33, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_head_pointer().add_tail_pointer(), 2, 10),
#         # (34, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 2, 10),
#         # (35, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE), 3, 10),
#         # (36, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null(), 3, 10),
#         # (37, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_head_pointer().add_tail_pointer(), 3, 10),
#         # (38, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer(), 3, 10),
#     ),
# )
# def test_insert_animation(
#     scene: Scene,
#     unique_value_for_caching_control_data: int,
#     sll: SinglyLinkedList,
#     index: int,
#     value: Any,
# ) -> None:
#     scene.add(sll)
#
#     def insert_node_into_sll(self):
#         return sll.animate.insert_node(
#             index,
#             value,
#             center=True,
#         )
#
#     scene.register_function(insert_node_into_sll)
#
#     scene.play()
#     # scene.play(
#     #     sll.animate.insert_node(
#     #         index,
#     #         value,
#     #         center=True,
#     #     )
#     # )


# @frames_comparison
# @pytest.mark.parametrize(
#
# )
# def test_insertion_to_empty_sll() -> None:
#     ...
#
#
# # TODO:
# #  1. Starting slls of lengths 0, 1, 2, 3
# #  2. With and without showing null
# #  3. Insertion at the head, tail, and in the middle
# #  4. Multiple insertions at a time
# @frames_comparison
# @pytest.mark.parametrize(
#     ("indices_and_values", "sll"),
#     (
#         ([(0, 5)], SinglyLinkedList()),
#         # ([(0, 5)], SinglyLinkedList(show_null=True)),
#     )
# )
# def test_insertion(scene: Scene, indices_and_values: Sequence[int, Any], sll: SinglyLinkedList) -> None:
#     for index, value in indices_and_values:
#         sll.insert_node(index, value)
#
#     scene.add(sll)
