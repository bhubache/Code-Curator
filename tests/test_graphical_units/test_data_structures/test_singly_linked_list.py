from __future__ import annotations

from typing import Any
from typing import TYPE_CHECKING

import pytest
from manim import DOWN
from manim import UP
from manim import WHITE

from code_curator.data_structures.singly_linked_list_v2 import SinglyLinkedList
from code_curator.utils.testing.curator_frames_comparison import curator_frames_comparison

if TYPE_CHECKING:
    from code_curator.base_scene import BaseScene
    from manim.typing import Vector


__module_test__ = "data_structures"


@curator_frames_comparison
@pytest.mark.parametrize(
    "kwargs",
    (
        {"color": WHITE},
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
class test_sll_building:
    def __init__(self, scene: BaseScene, kwargs: dict[str, Any]) -> None:
        self.scene = scene

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
    ("unique_value", "sll"),
    (
        (0, SinglyLinkedList.create_sll(color=WHITE)),
        (2, SinglyLinkedList.create_sll(color=WHITE).add_null()),
        (3, SinglyLinkedList.create_sll(color=WHITE).add_null().add_head_pointer().add_tail_pointer()),
        (4, SinglyLinkedList.create_sll(0, color=WHITE)),
        (5, SinglyLinkedList.create_sll(0, color=WHITE).add_head_pointer().add_tail_pointer()),
        (6, SinglyLinkedList.create_sll(0, color=WHITE).add_null()),
        (7, SinglyLinkedList.create_sll(0, color=WHITE).add_null().add_head_pointer().add_tail_pointer()),
        (8, SinglyLinkedList.create_sll(0, 1, color=WHITE)),
        (9, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_head_pointer().add_tail_pointer()),
        (10, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null()),
        (11, SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer()),
    ),
)
class test_adding_null_node:
    def __init__(self, scene, unique_value, sll) -> None:
        self.scene = scene
        self.sll = sll

    def my_animation(self):
        self.scene.add(self.sll)
        return self.sll.animate.add_null()


@curator_frames_comparison(last_frame=False)
@pytest.mark.parametrize(
    (
        "unique_value_for_caching_control_data",
        "sll",
        "starting_index",
        "ending_index",
        "starting_pointer_direction",
        "ending_pointer_direction",
    ),
    (
        (1, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null(), 0, 0, UP, UP),
        (2, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null(), 0, 0, UP, DOWN),
        (3, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null(), 0, 0, DOWN, UP),
        (4, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null(), 0, 1, UP, UP),
        (5, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null(), 0, 1, UP, DOWN),
        (6, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null(), 0, 1, DOWN, UP),
        (8, SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null(), 0, "null", UP, UP),
    ),
)
class test_move_pointer:
    def __init__(
        self,
        scene: BaseScene,
        unique_value_for_caching_control_data: int,
        sll: SinglyLinkedList,
        starting_index: int,
        ending_index: int,
        starting_pointer_direction: Vector,
        ending_pointer_direction: Vector,
    ) -> None:
        self.scene = scene
        self.sll = sll
        self.ending_index = ending_index
        self.ending_pointer_direction = ending_pointer_direction

        if starting_index == "null":
            starting_node = self.sll.null
        else:
            starting_node = self.sll[starting_index]

        self.sll.add_labeled_pointer(starting_node, label="pointer", direction=starting_pointer_direction)
        self.scene.add(self.sll)

    def animation(self):
        if self.ending_index == "null":
            to_node = self.sll.null
        else:
            to_node = self.sll[self.ending_index]

        return self.sll.animate.move_labeled_pointer(
            "pointer",
            to_node,
            pointer_direction=self.ending_pointer_direction,
        )


@curator_frames_comparison(last_frame=False)
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
class test_insert_node:
    def __init__(
        self,
        scene: BaseScene,
        unique_value_for_caching_control_data: int,
        sll: SinglyLinkedList,
        index: int,
        value: Any,
    ) -> None:
        self.scene = scene
        self.sll = sll
        self.index = index
        self.value = value

        self.scene.add(self.sll)

    def animation(self):
        return self.sll.animate.insert_node(
            self.index,
            self.value,
            center=True,
        )
