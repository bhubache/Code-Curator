from __future__ import annotations

import pytest
from manim import DOWN
from manim import WHITE

from code_curator.data_structures.singly_linked_list import SinglyLinkedList


def validate_sll(
    sll: SinglyLinkedList,
    *values,
    has_null: bool,
    has_head_pointer: bool,
    has_tail_pointer: bool,
    color,
) -> None:
    assert len(sll) == len(values)
    assert len(sll.nodes) == len(values)
    assert len(sll.values) == len(values)
    assert sll.color == color

    if values or has_null:
        assert sll.has_head
        assert sll.has_tail

        if values:
            assert sll.head is sll.get_node(0)
            assert sll.tail is sll.get_node(-1)
        elif has_null:
            assert sll.head is sll.null
            assert sll.tail is sll.null
    else:
        assert not sll.has_head
        assert not sll.has_tail

    if has_null:
        assert sll.has_null
    else:
        assert not sll.has_null

    if has_head_pointer:
        assert sll.has_head_pointer
        assert sll.head_pointer_pointee is sll.head
    else:
        assert not sll.has_head_pointer

    if has_tail_pointer:
        assert sll.has_tail_pointer
        assert sll.tail_pointer_pointee is sll.tail
    else:
        assert not sll.has_tail_pointer

    for index, val in enumerate(values):
        assert sll.get_node(index).value == val

    assert sll.get_prev(sll.head) is None

    for index, node in enumerate(sll):
        assert node.value == values[index]

    for index, _ in enumerate(values):
        if index > 0:
            assert sll.get_prev(sll.get_node(index)).value == values[index - 1]

        if index < len(values) - 1:
            assert sll.get_next(sll.get_node(index)).value == values[index + 1]

    if values:
        if has_null:
            assert sll.get_next(sll.get_node(-1)) is sll.null
            assert not sll.has_next(sll.null)
        else:
            assert not sll.has_next(sll.get_node(-1))
    else:
        if has_null:
            assert not sll.has_next(sll.null)


def test_empty_sll() -> None:
    sll = SinglyLinkedList.create_sll(color=WHITE)

    validate_sll(sll, has_null=False, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


def test_empty_sll_with_pointers() -> None:
    with pytest.raises(RuntimeError):
        SinglyLinkedList.create_sll(color=WHITE).add_head_pointer()

    with pytest.raises(RuntimeError):
        SinglyLinkedList.create_sll(color=WHITE).add_tail_pointer()


def test_empty_sll_showing_null() -> None:
    sll = SinglyLinkedList.create_sll(color=WHITE).add_null()

    validate_sll(sll, has_null=True, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


def test_empty_sll_showing_null_with_pointers() -> None:
    sll = SinglyLinkedList.create_sll(color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    validate_sll(sll, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_one_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, color=WHITE)

    validate_sll(sll, 0, has_null=False, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


def test_one_node_sll_with_pointers() -> None:
    sll = SinglyLinkedList.create_sll(0, color=WHITE).add_head_pointer().add_tail_pointer()

    validate_sll(sll, 0, has_null=False, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_one_node_sll_showing_null() -> None:
    sll = SinglyLinkedList.create_sll(0, color=WHITE).add_null()

    validate_sll(sll, 0, has_null=True, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


def test_one_node_sll_showing_null_with_pointers() -> None:
    sll = SinglyLinkedList.create_sll(0, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    validate_sll(sll, 0, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_two_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE)

    validate_sll(sll, 0, 1, has_null=False, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


def test_two_node_sll_showing_pointers() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE).add_head_pointer().add_tail_pointer()

    validate_sll(sll, 0, 1, has_null=False, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_two_node_sll_showing_null() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null()

    validate_sll(sll, 0, 1, has_null=True, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


def test_two_node_sll_showing_null_showing_pointers() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    validate_sll(sll, 0, 1, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_three_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE)

    validate_sll(sll, 0, 1, 2, has_null=False, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


def test_three_node_sll_with_pointers() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_head_pointer().add_tail_pointer()

    validate_sll(sll, 0, 1, 2, has_null=False, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_three_node_sll_showing_null() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null()

    validate_sll(sll, 0, 1, 2, has_null=True, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


def test_three_node_sll_showing_null_with_pointers() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    validate_sll(sll, 0, 1, 2, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_insert_into_empty_sll() -> None:
    sll = SinglyLinkedList.create_sll(color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    sll.insert_node(len(sll), 10)

    validate_sll(sll, 10, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_insert_at_front_of_one_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    sll.insert_node(0, 10)

    validate_sll(sll, 10, 0, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_insert_at_end_of_one_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    sll.insert_node(1, 10)

    validate_sll(sll, 0, 10, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_insert_at_front_of_two_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    sll.insert_node(0, 10)

    validate_sll(sll, 10, 0, 1, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_insert_at_end_of_two_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    sll.insert_node(2, 10)

    validate_sll(sll, 0, 1, 10, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_insert_in_middle_of_two_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    sll.insert_node(1, 10)

    validate_sll(sll, 0, 10, 1, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_insert_at_front_of_three_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    sll.insert_node(0, 10)

    validate_sll(sll, 10, 0, 1, 2, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_insert_at_end_of_three_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    sll.insert_node(3, 10)

    validate_sll(sll, 0, 1, 2, 10, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_insert_at_index_one_of_three_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    sll.insert_node(1, 10)

    validate_sll(sll, 0, 10, 1, 2, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_insert_at_index_two_of_three_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    sll.insert_node(2, 10)

    validate_sll(sll, 0, 1, 10, 2, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_add_null_node_to_non_empty_sll() -> None:
    sll = SinglyLinkedList(0, color=WHITE)

    return_value = sll.add_null()

    assert return_value is sll
    validate_sll(sll, 0, has_null=True, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


def test_add_null_node_to_empty_sll() -> None:
    sll = SinglyLinkedList.create_sll(color=WHITE)

    return_value = sll.add_null()

    assert return_value is sll
    validate_sll(sll, has_null=True, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


def test_add_null_node_to_sll_that_already_has_null() -> None:
    sll = SinglyLinkedList.create_sll(color=WHITE).add_null()

    return_value = sll.add_null()

    assert return_value is sll
    validate_sll(sll, has_null=True, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


def test_getting_heads_next_node() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null()

    next_node = sll.get_next(sll.head)

    assert next_node.value == 1


def test_getting_middles_next_node() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null()

    next_node = sll.get_next(sll[1])

    assert next_node.value == 2


def test_getting_tails_next_node_without_null() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE)

    next_node = sll.get_next(sll.tail)

    assert next_node is None


def test_getting_tail_next_node_with_null() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null()

    next_node = sll.get_next(sll.tail)

    assert next_node.value == "null"


def test_getting_nulls_next_node() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null()

    next_node = sll.get_next(sll.null)

    assert next_node is None


def test_head_has_next_node() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null()

    assert sll.has_next(sll.head)


def test_tail_has_next_node() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null()

    assert sll.has_next(sll.tail)


def test_tail_does_not_have_next_node() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE)

    assert not sll.has_next(sll.tail)


def test_null_does_not_have_next_node() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null()

    assert not sll.has_next(sll.null)


def test_setting_next_node_to_current_next_node() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE)
    original_next = sll.get_next(sll.head)

    sll.set_next(sll.head, original_next)

    assert sll.get_next(sll.head) is original_next
    assert len(sll) == 3


def test_setting_next_node_to_adjacent_right_node() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE)
    original_head = sll.head
    original_tail = sll.tail

    sll.set_next(sll.head, sll.tail)

    assert sll.head is original_head
    assert sll.tail is original_tail
    # validate_sll(sll, 0, 2, has_null=False, has_head_pointer=False, has_tail_pointer=False, color=WHITE)
    assert sll.get_next(sll.head) is sll.tail
    assert len(sll) == 2


def test_setting_next_node_to_next_next_node() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null()

    sll.set_next(sll.head, sll.null)

    assert sll.get_next(sll.head) is sll.null
    assert len(sll) == 1


def test_cutting_out_tail_with_set_next() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null()
    node_whose_pointer_is_changing = sll.get_prev(sll.tail)

    sll.set_next(node_whose_pointer_is_changing, sll.null)

    assert sll.get_next(node_whose_pointer_is_changing) is sll.null
    assert sll.tail is node_whose_pointer_is_changing
    assert len(sll) == 2


def test_removing_from_empty_sll_raises_exception() -> None:
    sll = SinglyLinkedList.create_sll(color=WHITE)

    with pytest.raises(IndexError):
        sll.remove_node(0)


def test_removing_from_one_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, color=WHITE)

    sll.remove_node(0)

    validate_sll(sll, has_null=False, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


def test_removing_from_one_node_sll_with_null() -> None:
    sll = SinglyLinkedList.create_sll(0, color=WHITE).add_null()

    sll.remove_node(0)

    validate_sll(sll, has_null=True, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


def test_removing_from_one_node_sll_with_null_and_head_and_tail_pointers() -> None:
    sll = SinglyLinkedList.create_sll(0, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    sll.remove_node(0)

    validate_sll(sll, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)


def test_removing_first_node_from_two_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE)

    sll.remove_node(0)

    validate_sll(sll, 1, has_null=False, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


def test_removing_second_node_from_two_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE)

    sll.remove_node(1)

    validate_sll(sll, 0, has_null=False, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


def test_removing_first_node_from_two_node_sll_with_null() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null()

    sll.remove_node(0)

    validate_sll(sll, 1, has_null=True, has_head_pointer=False, has_tail_pointer=False, color=WHITE)


@pytest.mark.parametrize(
    (
        "values",
        "remove_at_index",
        "color",
        "initially_has_null",
        "initially_has_head_pointer",
        "initially_has_tail_pointer",
        "post_removal_has_null",
        "post_removal_has_head_pointer",
        "post_removal_has_tail_pointer",
    ),
    (
        ([0], 0, WHITE, False, False, False, False, False, False),
        ([0], 0, WHITE, True, False, False, True, False, False),
        ([0], 0, WHITE, False, True, False, False, False, False),
        ([0], 0, WHITE, False, False, True, False, False, False),
        ([0], 0, WHITE, True, True, False, True, True, False),
        ([0], 0, WHITE, True, False, True, True, False, True),
        ([0], 0, WHITE, False, True, True, False, False, False),
        ([0], 0, WHITE, True, True, True, True, True, True),
        ([0, 1], 0, WHITE, False, False, False, False, False, False),
        ([0, 1], 0, WHITE, True, False, False, True, False, False),
        ([0, 1], 0, WHITE, False, True, False, False, True, False),
        ([0, 1], 0, WHITE, False, False, True, False, False, True),
        ([0, 1], 0, WHITE, True, True, False, True, True, False),
        ([0, 1], 0, WHITE, True, False, True, True, False, True),
        ([0, 1], 0, WHITE, False, True, True, False, True, True),
        ([0, 1], 0, WHITE, True, True, True, True, True, True),
        ([0, 1], 1, WHITE, False, False, False, False, False, False),
        ([0, 1], 1, WHITE, True, False, False, True, False, False),
        ([0, 1], 1, WHITE, False, True, False, False, True, False),
        ([0, 1], 1, WHITE, False, False, True, False, False, True),
        ([0, 1], 1, WHITE, True, True, False, True, True, False),
        ([0, 1], 1, WHITE, True, False, True, True, False, True),
        ([0, 1], 1, WHITE, False, True, True, False, True, True),
        ([0, 1], 1, WHITE, True, True, True, True, True, True),
        ([0, 1, 2], 0, WHITE, False, False, False, False, False, False),
        ([0, 1, 2], 0, WHITE, True, False, False, True, False, False),
        ([0, 1, 2], 0, WHITE, False, True, False, False, True, False),
        ([0, 1, 2], 0, WHITE, False, False, True, False, False, True),
        ([0, 1, 2], 0, WHITE, True, True, False, True, True, False),
        ([0, 1, 2], 0, WHITE, True, False, True, True, False, True),
        ([0, 1, 2], 0, WHITE, False, True, True, False, True, True),
        ([0, 1, 2], 0, WHITE, True, True, True, True, True, True),
        ([0, 1, 2], 1, WHITE, False, False, False, False, False, False),
        ([0, 1, 2], 1, WHITE, True, False, False, True, False, False),
        ([0, 1, 2], 1, WHITE, False, True, False, False, True, False),
        ([0, 1, 2], 1, WHITE, False, False, True, False, False, True),
        ([0, 1, 2], 1, WHITE, True, True, False, True, True, False),
        ([0, 1, 2], 1, WHITE, True, False, True, True, False, True),
        ([0, 1, 2], 1, WHITE, False, True, True, False, True, True),
        ([0, 1, 2], 1, WHITE, True, True, True, True, True, True),
        ([0, 1, 2], 2, WHITE, False, False, False, False, False, False),
        ([0, 1, 2], 2, WHITE, True, False, False, True, False, False),
        ([0, 1, 2], 2, WHITE, False, True, False, False, True, False),
        ([0, 1, 2], 2, WHITE, False, False, True, False, False, True),
        ([0, 1, 2], 2, WHITE, True, True, False, True, True, False),
        ([0, 1, 2], 2, WHITE, True, False, True, True, False, True),
        ([0, 1, 2], 2, WHITE, False, True, True, False, True, True),
        ([0, 1, 2], 2, WHITE, True, True, True, True, True, True),
    ),
)
def test_removing_node(
    values,
    remove_at_index,
    color,
    initially_has_null,
    initially_has_head_pointer,
    initially_has_tail_pointer,
    post_removal_has_null,
    post_removal_has_head_pointer,
    post_removal_has_tail_pointer,
) -> None:
    sll = SinglyLinkedList.create_sll(*values, color=color)

    if initially_has_null:
        sll.add_null()

    if initially_has_head_pointer:
        sll.add_head_pointer()

    if initially_has_tail_pointer:
        sll.add_tail_pointer()

    sll.remove_node(remove_at_index)

    new_values = values
    new_values.pop(remove_at_index)

    validate_sll(
        sll,
        *new_values,
        has_null=post_removal_has_null,
        has_head_pointer=post_removal_has_head_pointer,
        has_tail_pointer=post_removal_has_tail_pointer,
        color=color,
    )


def test_adding_node() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    node_to_add = sll.create_node(10)
    node_to_add.next_to(sll[1], DOWN)

    sll.add(node_to_add)

    validate_sll(sll, 0, 1, has_null=True, has_head_pointer=True, has_tail_pointer=True, color=WHITE)
