from __future__ import annotations

from typing import Any

import pytest
from manim import Scene
from manim import WHITE
from manim.utils.testing.frames_comparison import frames_comparison

from code_curator.data_structures.singly_linked_list_v2 import SinglyLinkedList


__module_test__ = "data_structures"


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
#         sll._insert_node(index, value)
#
#     scene.add(sll)
