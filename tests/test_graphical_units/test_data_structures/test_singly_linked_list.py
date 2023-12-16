from __future__ import annotations

from typing import Any

import pytest
from manim import DOWN
from manim import Scene
from manim import UP
from manim import WHITE
from manim.typing import Vector
from manim.utils.testing.frames_comparison import frames_comparison
from tests.scenes import MockBaseScene

from code_curator.data_structures.singly_linked_list_v2 import SinglyLinkedList


__module_test__ = "data_structures"


@frames_comparison(base_scene=MockBaseScene)
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


@frames_comparison(base_scene=MockBaseScene)
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
    base_scene=MockBaseScene.set_run_time(1.0).add_animation_method("move_head_pointer", start_time=0.0),
)
@pytest.mark.parametrize(
    ("unique_value_for_caching_control_data", "sll", "index", "pointer_direction"),
    (
        (1, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer(), 1, DOWN),
        (1, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer(), 2, DOWN),
        (1, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer(), "null", DOWN),
        (1, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer(), 1, UP),
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
