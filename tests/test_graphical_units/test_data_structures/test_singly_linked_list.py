from __future__ import annotations

from typing import Any
from typing import TYPE_CHECKING

import pytest
from manim import DOWN
from manim import UP
from manim import WHITE

from code_curator.data_structures.singly_linked_list import SinglyLinkedList
from code_curator.utils.testing.curator_frames_comparison import curator_frames_comparison

if TYPE_CHECKING:
    from code_curator.base_scene import BaseScene
    from manim.typing import Vector
    from manim import ParsableManimColor
    from collections.abc import Sequence


__module_test__ = "singly_linked_list"


@curator_frames_comparison
@pytest.mark.parametrize(
    ("values", "color", "add_null", "add_head_pointer", "add_tail_pointer"),
    (
        ([], WHITE, False, False, False),
        ([], WHITE, True, False, False),
        ([], WHITE, True, True, True),
        ([0], WHITE, False, False, False),
        ([0], WHITE, True, False, False),
        ([0], WHITE, False, True, True),
        ([0], WHITE, True, True, True),
        ([0, 1], WHITE, False, False, False),
        ([0, 1], WHITE, True, False, False),
        ([0, 1], WHITE, False, True, True),
        ([0, 1], WHITE, True, True, True),
        ([0, 1, 2], WHITE, False, False, False),
        ([0, 1, 2], WHITE, True, False, False),
        ([0, 1, 2], WHITE, False, True, True),
        ([0, 1, 2], WHITE, True, True, True),
    ),
)
class test_sll_building:
    def __init__(
        self,
        scene: BaseScene,
        values: Sequence[Any],
        color: ParsableManimColor,
        add_null: bool,
        add_head_pointer: bool,
        add_tail_pointer: bool,
    ) -> None:
        self.scene = scene

        sll = SinglyLinkedList.create_sll(*values, color=color)

        if add_null:
            sll.add_null()

        if add_head_pointer:
            sll.add_head_pointer()

        if add_tail_pointer:
            sll.add_tail_pointer()

        scene.add(sll)


@curator_frames_comparison(last_frame=False)
@pytest.mark.parametrize(
    ("values", "color", "add_null", "add_head_pointer", "add_tail_pointer"),
    (
        ([], WHITE, False, False, False),
        ([], WHITE, True, False, False),
        ([], WHITE, True, True, True),
        ([0], WHITE, False, False, False),
        ([0], WHITE, False, True, True),
        ([0], WHITE, True, False, False),
        ([0], WHITE, True, True, True),
        ([0, 1], WHITE, False, False, False),
        ([0, 1], WHITE, False, True, True),
        ([0, 1], WHITE, True, False, False),
        ([0, 1], WHITE, True, True, True),
    ),
)
class test_adding_null_node:
    def __init__(
        self,
        scene,
        values: Sequence[Any],
        color: ParsableManimColor,
        add_null: bool,
        add_head_pointer: bool,
        add_tail_pointer: bool,
    ) -> None:
        self.scene = scene
        self.sll = SinglyLinkedList.create_sll(*values, color=color)

        if add_null:
            self.sll.add_null()

        if add_head_pointer:
            self.sll.add_head_pointer()

        if add_tail_pointer:
            self.sll.add_tail_pointer()

    def my_animation(self):
        self.scene.add(self.sll)
        return self.sll.animate.add_null()


@curator_frames_comparison(last_frame=False)
@pytest.mark.parametrize(
    (
        "values",
        "color",
        "add_null",
        "add_head_pointer",
        "add_tail_pointer",
        "start_index",
        "end_index",
        "start_pointer_direction",
        "end_pointer_direction",
    ),
    (
        ([0, 1, 2], WHITE, True, False, False, 0, 0, UP, UP),
        ([0, 1, 2], WHITE, True, False, False, 0, 0, UP, DOWN),
        ([0, 1, 2], WHITE, True, False, False, 0, 0, DOWN, UP),
        ([0, 1, 2], WHITE, True, False, False, 0, 1, UP, UP),
        ([0, 1, 2], WHITE, True, False, False, 0, 1, UP, DOWN),
        ([0, 1, 2], WHITE, True, False, False, 0, 1, DOWN, UP),
        ([0, 1, 2], WHITE, True, False, False, 0, "null", UP, UP),
    ),
)
class test_move_pointer:
    def __init__(
        self,
        scene: BaseScene,
        values: Sequence[Any],
        color: ParsableManimColor,
        add_null: bool,
        add_head_pointer: bool,
        add_tail_pointer: bool,
        start_index: int,
        end_index: int,
        start_pointer_direction: Vector,
        end_pointer_direction: Vector,
    ) -> None:
        self.scene = scene
        self.end_index = end_index
        self.end_pointer_direction = end_pointer_direction

        self.sll = SinglyLinkedList.create_sll(*values, color=color)

        if add_null:
            self.sll.add_null()

        if add_head_pointer:
            self.sll.add_head_pointer()

        if add_tail_pointer:
            self.sll.add_tail_pointer()

        if start_index == "null":
            start_node = self.sll.null
        else:
            start_node = self.sll[start_index]

        self.sll.add_labeled_pointer(start_node, label="pointer", direction=start_pointer_direction)
        self.scene.add(self.sll)

    def animation(self):
        if self.end_index == "null":
            to_node = self.sll.null
        else:
            to_node = self.sll[self.end_index]

        return self.sll.animate.move_labeled_pointer(
            "pointer",
            to_node,
            pointer_direction=self.end_pointer_direction,
        )


@curator_frames_comparison(last_frame=False)
@pytest.mark.parametrize(
    ("values", "color", "add_null", "add_head_pointer", "add_tail_pointer", "index", "value"),
    (
        # Empty
        ([], WHITE, False, False, False, 0, 10),
        ([], WHITE, True, False, False, 0, 10),
        ([], WHITE, True, True, True, 0, 10),
        # One node
        ([0], WHITE, False, False, False, 0, 10),
        ([0], WHITE, True, False, False, 0, 10),
        ([0], WHITE, False, True, True, 0, 10),
        ([0], WHITE, True, True, True, 0, 10),
        ([0], WHITE, False, False, False, 1, 10),
        ([0], WHITE, True, False, False, 1, 10),
        ([0], WHITE, False, True, True, 1, 10),
        ([0], WHITE, True, True, True, 1, 10),
        # Two nodes
        ([0, 1], WHITE, False, False, False, 0, 10),
        ([0, 1], WHITE, True, False, False, 0, 10),
        ([0, 1], WHITE, False, True, True, 0, 10),
        ([0, 1], WHITE, True, True, True, 0, 10),
        ([0, 1], WHITE, False, False, False, 1, 10),
        ([0, 1], WHITE, True, False, False, 1, 10),
        ([0, 1], WHITE, False, True, True, 1, 10),
        ([0, 1], WHITE, True, True, True, 1, 10),
        ([0, 1], WHITE, False, False, False, 2, 10),
        ([0, 1], WHITE, True, False, False, 2, 10),
        ([0, 1], WHITE, False, True, True, 2, 10),
        ([0, 1], WHITE, True, True, True, 2, 10),
        # Three nodes
        ([0, 1, 2], WHITE, False, False, False, 0, 10),
        ([0, 1, 2], WHITE, True, False, False, 0, 10),
        ([0, 1, 2], WHITE, False, True, True, 0, 10),
        ([0, 1, 2], WHITE, True, True, True, 0, 10),
        ([0, 1, 2], WHITE, False, False, False, 1, 10),
        ([0, 1, 2], WHITE, True, False, False, 1, 10),
        ([0, 1, 2], WHITE, False, True, True, 1, 10),
        ([0, 1, 2], WHITE, True, True, True, 1, 10),
        ([0, 1, 2], WHITE, False, False, False, 2, 10),
        ([0, 1, 2], WHITE, True, False, False, 2, 10),
        ([0, 1, 2], WHITE, False, True, True, 2, 10),
        ([0, 1, 2], WHITE, True, True, True, 2, 10),
        ([0, 1, 2], WHITE, False, False, False, 3, 10),
        ([0, 1, 2], WHITE, True, False, False, 3, 10),
        ([0, 1, 2], WHITE, False, True, True, 3, 10),
        ([0, 1, 2], WHITE, True, True, True, 3, 10),
    ),
)
class test_insert_node:
    def __init__(
        self,
        scene: BaseScene,
        values: Sequence[Any],
        color: ParsableManimColor,
        add_null: bool,
        add_head_pointer: bool,
        add_tail_pointer: bool,
        index: int,
        value: Any,
    ) -> None:
        self.scene = scene
        self.index = index
        self.value = value

        self.sll = SinglyLinkedList.create_sll(*values, color=color)

        if add_null:
            self.sll.add_null()

        if add_head_pointer:
            self.sll.add_head_pointer()

        if add_tail_pointer:
            self.sll.add_tail_pointer()

        self.scene.add(self.sll)

    def animation(self):
        return self.sll.animate.insert_node(
            self.index,
            self.value,
            center=True,
        )


@curator_frames_comparison(last_frame=False)
@pytest.mark.parametrize(
    (
        "values",
        "remove_at_index",
        "color",
        "initially_has_null",
        "initially_has_head_pointer",
        "initially_has_tail_pointer",
    ),
    (
        ([0], 0, WHITE, False, False, False),
        ([0], 0, WHITE, True, False, False),
        ([0], 0, WHITE, False, True, False),
        ([0], 0, WHITE, False, False, True),
        ([0], 0, WHITE, True, True, False),
        ([0], 0, WHITE, True, False, True),
        ([0], 0, WHITE, False, True, True),
        ([0], 0, WHITE, True, True, True),
        ([0, 1], 0, WHITE, False, False, False),
        ([0, 1], 0, WHITE, True, False, False),
        ([0, 1], 0, WHITE, False, True, False),
        ([0, 1], 0, WHITE, False, False, True),
        ([0, 1], 0, WHITE, True, True, False),
        ([0, 1], 0, WHITE, True, False, True),
        ([0, 1], 0, WHITE, False, True, True),
        ([0, 1], 0, WHITE, True, True, True),
        ([0, 1], 1, WHITE, False, False, False),
        ([0, 1], 1, WHITE, True, False, False),
        ([0, 1], 1, WHITE, False, True, False),
        ([0, 1], 1, WHITE, False, False, True),
        ([0, 1], 1, WHITE, True, True, False),
        ([0, 1], 1, WHITE, True, False, True),
        ([0, 1], 1, WHITE, False, True, True),
        ([0, 1], 1, WHITE, True, True, True),
        ([0, 1, 2], 0, WHITE, False, False, False),
        ([0, 1, 2], 0, WHITE, True, False, False),
        ([0, 1, 2], 0, WHITE, False, True, False),
        ([0, 1, 2], 0, WHITE, False, False, True),
        ([0, 1, 2], 0, WHITE, True, True, False),
        ([0, 1, 2], 0, WHITE, True, False, True),
        ([0, 1, 2], 0, WHITE, False, True, True),
        ([0, 1, 2], 0, WHITE, True, True, True),
        ([0, 1, 2], 1, WHITE, False, False, False),
        ([0, 1, 2], 1, WHITE, True, False, False),
        ([0, 1, 2], 1, WHITE, False, True, False),
        ([0, 1, 2], 1, WHITE, False, False, True),
        ([0, 1, 2], 1, WHITE, True, True, False),
        ([0, 1, 2], 1, WHITE, True, False, True),
        ([0, 1, 2], 1, WHITE, False, True, True),
        ([0, 1, 2], 1, WHITE, True, True, True),
        ([0, 1, 2], 2, WHITE, False, False, False),
        ([0, 1, 2], 2, WHITE, True, False, False),
        ([0, 1, 2], 2, WHITE, False, True, False),
        ([0, 1, 2], 2, WHITE, False, False, True),
        ([0, 1, 2], 2, WHITE, True, True, False),
        ([0, 1, 2], 2, WHITE, True, False, True),
        ([0, 1, 2], 2, WHITE, False, True, True),
        ([0, 1, 2], 2, WHITE, True, True, True),
    ),
)
class test_remove_node:
    def __init__(
        self,
        scene: BaseScene,
        values,
        remove_at_index: int,
        color,
        initially_has_null: bool,
        initially_has_head_pointer: bool,
        initially_has_tail_pointer: bool,
    ) -> None:
        sll = SinglyLinkedList.create_sll(*values, color=color)
        scene.add(sll)

        if initially_has_null:
            sll.add_null()

        if initially_has_head_pointer:
            sll.add_head_pointer()

        if initially_has_tail_pointer:
            sll.add_tail_pointer()

        self.sll = sll
        self.remove_at_index = remove_at_index

    def animation(self):
        return self.sll.animate.remove_node(self.remove_at_index)


@curator_frames_comparison(last_frame=False)
class test_add_node:
    def __init__(self, scene: BaseScene) -> None:
        self.sll = SinglyLinkedList(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer()
        scene.add(self.sll)

        self.node_to_add = self.sll.create_node(10)
        self.node_to_add.next_to(self.sll[1], DOWN)

    def animation(self):
        return self.sll.animate.add(self.node_to_add)


@curator_frames_comparison(last_frame=False)
class test_flatten_already_flattened_sll:
    def __init__(self, scene: BaseScene) -> None:
        self.sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer()
        scene.add(self.sll)

    def animation(self):
        return self.sll.animate.flatten(center=True)


@curator_frames_comparison(last_frame=False)
class test_flatten_one_node_sll:
    def __init__(self, scene: BaseScene) -> None:
        self.sll = SinglyLinkedList.create_sll(0, color=WHITE).add_head_pointer().add_tail_pointer()
        scene.add(self.sll)

        self.sll.move_to((2, 2, 0))

    def animation(self):
        return self.sll.animate.flatten(center=True)


@curator_frames_comparison(last_frame=False)
class test_flatten_sll_with_curved_next_pointer:
    def __init__(self, scene: BaseScene) -> None:
        self.sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer()
        scene.add(self.sll)

        pointer_to_remove = self.sll.get_next_pointer(self.sll[1])
        node_to_remove = self.sll.get_node(1)

        self.sll.set_next(self.sll.head, self.sll.tail, angle_in_degrees=90)
        self.sll.remove(pointer_to_remove)
        self.sll.remove(node_to_remove)

    def animation(self):
        return self.sll.animate.flatten(center=True)


# @curator_frames_comparison(last_frame=False)
# class test_flatten_sll_with_scattered_nodes:
#     def __init__(self, scene: BaseScene) -> None:
#         self.sll = SinglyLinkedList.create_sll(0, 1, 2, 3, color=WHITE).add_null().add_head_pointer().add_tail_pointer()
#         scene.add(self.sll)
#
#         self.sll[0].move_to((2, 2, 0))
#         self.sll[1].move_to((-3, 1, 0))
#         self.sll[2].move_to((0, -2, 0))
#         # self.sll.force_update()
#         self.sll.resume_updating()
#
#     def animation(self):
#         return self.sll.animate.flatten(center=True)


# Flatten:
# 1. SLL with nodes scattered around
# 3. SLL with nodes scattered around and curved next pointer
