from __future__ import annotations

import pytest
from manim import WHITE

from code_curator.data_structures.singly_linked_list_v2 import SinglyLinkedList

# TODO: Test with head, tail, and head and tail pointers, test directions of the pointers


def test_empty_sll() -> None:
    sll = SinglyLinkedList.create_sll(color=WHITE)

    assert len(sll) == 0
    assert len(sll.values) == 0
    assert len(sll.nodes) == 0
    assert sll.color == WHITE
    assert sll.has_null is False
    assert sll.has_head is False
    assert sll.has_tail is False
    assert sll.has_head_pointer is False
    assert sll.has_tail_pointer is False
    with pytest.raises(IndexError):
        sll.get_node(0)


def test_empty_sll_with_pointers() -> None:
    with pytest.raises(RuntimeError):
        SinglyLinkedList.create_sll(color=WHITE).add_head_pointer()

    with pytest.raises(RuntimeError):
        SinglyLinkedList.create_sll(color=WHITE).add_tail_pointer()


def test_empty_sll_showing_null() -> None:
    sll = SinglyLinkedList.create_sll(color=WHITE).add_null()

    assert len(sll) == 0
    assert len(sll.values) == 0
    assert len(sll.nodes) == 0
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is sll.tail
    assert sll.head is sll.null
    assert sll.has_head_pointer is False
    assert sll.has_tail_pointer is False
    with pytest.raises(IndexError):
        sll.get_node(0)


def test_empty_sll_showing_null_with_pointers() -> None:
    sll = SinglyLinkedList.create_sll(color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    assert len(sll) == 0
    assert len(sll.values) == 0
    assert len(sll.nodes) == 0
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is sll.tail
    assert sll.head is sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    with pytest.raises(IndexError):
        sll.get_node(0)


def test_one_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, color=WHITE)

    assert len(sll) == 1
    assert len(sll.values) == 1
    assert len(sll.nodes) == 1
    assert sll.color == WHITE
    assert sll.has_null is False
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is sll.tail
    assert sll.head is not sll.null
    assert sll.has_head_pointer is False
    assert sll.has_tail_pointer is False
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert not sll.has_next(sll.get_node(0))
    assert sll.get_prev(sll.get_node(0)) is None
    with pytest.raises(IndexError):
        sll.get_node(1)


def test_one_node_sll_with_pointers() -> None:
    sll = SinglyLinkedList.create_sll(0, color=WHITE).add_head_pointer().add_tail_pointer()

    assert len(sll) == 1
    assert len(sll.values) == 1
    assert len(sll.nodes) == 1
    assert sll.color == WHITE
    assert sll.has_null is False
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is sll.tail
    assert sll.head is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert not sll.has_next(sll.get_node(0))
    assert sll.get_prev(sll.get_node(0)) is None
    with pytest.raises(IndexError):
        sll.get_node(1)


def test_one_node_sll_showing_null() -> None:
    sll = SinglyLinkedList.create_sll(0, color=WHITE).add_null()

    assert len(sll) == 1
    assert len(sll.values) == 1
    assert len(sll.nodes) == 1
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is sll.tail
    assert sll.head is not sll.null
    assert sll.has_head_pointer is False
    assert sll.has_tail_pointer is False
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_next(sll.get_node(0)) is sll.null
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_prev(sll.null) is sll.get_node(0)
    with pytest.raises(IndexError):
        sll.get_node(1)


def test_one_node_sll_showing_null_with_pointers() -> None:
    sll = SinglyLinkedList.create_sll(0, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    assert len(sll) == 1
    assert len(sll.values) == 1
    assert len(sll.nodes) == 1
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is sll.tail
    assert sll.head is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_next(sll.get_node(0)) is sll.null
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_prev(sll.null) is sll.get_node(0)
    with pytest.raises(IndexError):
        sll.get_node(1)


def test_two_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE)

    assert len(sll) == 2
    assert len(sll.values) == 2
    assert len(sll.nodes) == 2
    assert sll.color == WHITE
    assert sll.has_null is False
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.has_head_pointer is False
    assert sll.has_tail_pointer is False
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 1
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert not sll.has_next(sll.get_node(1))
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    with pytest.raises(IndexError):
        sll.get_node(2)


def test_two_node_sll_showing_pointers() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE).add_head_pointer().add_tail_pointer()

    assert len(sll) == 2
    assert len(sll.values) == 2
    assert len(sll.nodes) == 2
    assert sll.color == WHITE
    assert sll.has_null is False
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 1
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert not sll.has_next(sll.get_node(1))
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    with pytest.raises(IndexError):
        sll.get_node(2)


def test_two_node_sll_showing_null() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null()

    assert len(sll) == 2
    assert len(sll.values) == 2
    assert len(sll.nodes) == 2
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.has_head_pointer is False
    assert sll.has_tail_pointer is False
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 1
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_next(sll.get_node(1)) is sll.null
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    assert not sll.has_next(sll.null)
    assert sll.get_prev(sll.null) is sll.get_node(1)
    with pytest.raises(IndexError):
        sll.get_node(2)


# TODO: Test order of adding head and tail?
def test_two_node_sll_showing_null_showing_pointers() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    assert len(sll) == 2
    assert len(sll.values) == 2
    assert len(sll.nodes) == 2
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 1
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_next(sll.get_node(1)) is sll.null
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    assert not sll.has_next(sll.null)
    assert sll.get_prev(sll.null) is sll.get_node(1)
    with pytest.raises(IndexError):
        sll.get_node(2)


def test_three_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE)

    assert len(sll) == 3
    assert len(sll.values) == 3
    assert len(sll.nodes) == 3
    assert sll.color == WHITE
    assert sll.has_null is False
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.has_head_pointer is False
    assert sll.has_tail_pointer is False
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 1
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_node(2).value == 2
    assert sll.get_node_index(sll.get_node(2)) == 2
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_next(sll.get_node(1)) is sll.get_node(2)
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    assert not sll.has_next(sll.get_node(2))
    assert sll.get_prev(sll.get_node(2)) is sll.get_node(1)
    with pytest.raises(IndexError):
        sll.get_node(3)


def test_three_node_sll_with_pointers() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_head_pointer().add_tail_pointer()

    assert len(sll) == 3
    assert len(sll.values) == 3
    assert len(sll.nodes) == 3
    assert sll.color == WHITE
    assert sll.has_null is False
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 1
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_node(2).value == 2
    assert sll.get_node_index(sll.get_node(2)) == 2
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_next(sll.get_node(1)) is sll.get_node(2)
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    assert not sll.has_next(sll.get_node(2))
    assert sll.get_prev(sll.get_node(2)) is sll.get_node(1)
    with pytest.raises(IndexError):
        sll.get_node(3)


def test_three_node_sll_showing_null() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null()

    assert len(sll) == 3
    assert len(sll.values) == 3
    assert len(sll.nodes) == 3
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.has_head_pointer is False
    assert sll.has_tail_pointer is False
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 1
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_node(2).value == 2
    assert sll.get_node_index(sll.get_node(2)) == 2
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_next(sll.get_node(1)) is sll.get_node(2)
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    assert sll.get_next(sll.get_node(2)) is sll.null
    assert sll.get_prev(sll.get_node(2)) is sll.get_node(1)
    assert not sll.has_next(sll.null)
    assert sll.get_prev(sll.null) is sll.get_node(2)
    with pytest.raises(IndexError):
        sll.get_node(3)


def test_three_node_sll_showing_null_with_pointers() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    assert len(sll) == 3
    assert len(sll.values) == 3
    assert len(sll.nodes) == 3
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 1
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_node(2).value == 2
    assert sll.get_node_index(sll.get_node(2)) == 2
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_next(sll.get_node(1)) is sll.get_node(2)
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    assert sll.get_next(sll.get_node(2)) is sll.null
    assert sll.get_prev(sll.get_node(2)) is sll.get_node(1)
    assert not sll.has_next(sll.null)
    assert sll.get_prev(sll.null) is sll.get_node(2)
    with pytest.raises(IndexError):
        sll.get_node(3)


# TODO: Assuming indices work as expected
def test_insert_into_empty_sll() -> None:
    sll = SinglyLinkedList.create_sll(color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    sll.insert_node(len(sll), 10)

    assert len(sll) == 1
    assert len(sll.values) == 1
    assert len(sll.nodes) == 1
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is sll.tail
    assert sll.head is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 10
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_next(sll.get_node(0)) is sll.null
    assert sll.get_prev(sll.get_node(0)) is None
    assert not sll.has_next(sll.null)
    assert sll.get_prev(sll.null) is sll.get_node(0)
    with pytest.raises(IndexError):
        sll.get_node(1)


def test_insert_at_front_of_one_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, color=WHITE).add_null().add_head_pointer().add_tail_pointer()

    sll.insert_node(0, 10)

    assert len(sll) == 2
    assert len(sll.values) == 2
    assert len(sll.nodes) == 2
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.tail is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 10
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 0
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_next(sll.get_node(1)) is sll.null
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    assert not sll.has_next(sll.null)
    assert sll.get_prev(sll.null) is sll.get_node(1)
    with pytest.raises(IndexError):
        sll.get_node(2)


def test_insert_at_end_of_one_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, color=WHITE).add_null().add_head_pointer().add_tail_pointer()
    sll.insert_node(1, 10)

    assert len(sll) == 2
    assert len(sll.values) == 2
    assert len(sll.nodes) == 2
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.tail is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 10
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_next(sll.get_node(1)) is sll.null
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    assert not sll.has_next(sll.null)
    assert sll.get_prev(sll.null) is sll.get_node(1)
    with pytest.raises(IndexError):
        sll.get_node(2)


def test_insert_at_front_of_two_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer()
    sll.insert_node(0, 10)

    assert len(sll) == 3
    assert len(sll.values) == 3
    assert len(sll.nodes) == 3
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.tail is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 10
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 0
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_node(2).value == 1
    assert sll.get_node_index(sll.get_node(2)) == 2
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_next(sll.get_node(1)) is sll.get_node(2)
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    assert sll.get_next(sll.get_node(2)) is sll.null
    assert sll.get_prev(sll.get_node(2)) is sll.get_node(1)
    assert not sll.has_next(sll.null)
    assert sll.get_prev(sll.null) is sll.get_node(2)
    with pytest.raises(IndexError):
        sll.get_node(3)


def test_insert_at_end_of_two_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer()
    sll.insert_node(2, 10)

    assert len(sll) == 3
    assert len(sll.values) == 3
    assert len(sll.nodes) == 3
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.tail is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 1
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_node(2).value == 10
    assert sll.get_node_index(sll.get_node(2)) == 2
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_next(sll.get_node(1)) is sll.get_node(2)
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    assert sll.get_next(sll.get_node(2)) is sll.null
    assert sll.get_prev(sll.get_node(2)) is sll.get_node(1)
    assert not sll.has_next(sll.null)
    assert sll.get_prev(sll.null) is sll.get_node(2)
    with pytest.raises(IndexError):
        sll.get_node(3)


def test_insert_in_middle_of_two_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, color=WHITE).add_null().add_head_pointer().add_tail_pointer()
    sll.insert_node(1, 10)

    assert len(sll) == 3
    assert len(sll.values) == 3
    assert len(sll.nodes) == 3
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.tail is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 10
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_node(2).value == 1
    assert sll.get_node_index(sll.get_node(2)) == 2
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_next(sll.get_node(1)) is sll.get_node(2)
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    assert sll.get_next(sll.get_node(2)) is sll.null
    assert sll.get_prev(sll.get_node(2)) is sll.get_node(1)
    assert not sll.get_next(sll.null)
    assert sll.get_prev(sll.null) is sll.get_node(2)
    with pytest.raises(IndexError):
        sll.get_node(3)


def test_insert_at_front_of_three_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer()
    sll.insert_node(0, 10)

    assert len(sll) == 4
    assert len(sll.values) == 4
    assert len(sll.nodes) == 4
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.tail is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 10
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 0
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_node(2).value == 1
    assert sll.get_node_index(sll.get_node(2)) == 2
    assert sll.get_node(3).value == 2
    assert sll.get_node_index(sll.get_node(3)) == 3
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_next(sll.get_node(1)) is sll.get_node(2)
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    assert sll.get_next(sll.get_node(2)) is sll.get_node(3)
    assert sll.get_prev(sll.get_node(2)) is sll.get_node(1)
    assert sll.get_next(sll.get_node(3)) is sll.null
    assert sll.get_prev(sll.get_node(3)) is sll.get_node(2)
    assert not sll.has_next(sll.null)
    assert sll.get_prev(sll.null) is sll.get_node(3)
    with pytest.raises(IndexError):
        sll.get_node(4)


def test_insert_at_end_of_three_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer()
    sll.insert_node(3, 10)

    assert len(sll) == 4
    assert len(sll.values) == 4
    assert len(sll.nodes) == 4
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.tail is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 1
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_node(2).value == 2
    assert sll.get_node_index(sll.get_node(2)) == 2
    assert sll.get_node(3).value == 10
    assert sll.get_node_index(sll.get_node(3)) == 3
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_next(sll.get_node(1)) is sll.get_node(2)
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    assert sll.get_next(sll.get_node(2)) is sll.get_node(3)
    assert sll.get_prev(sll.get_node(2)) is sll.get_node(1)
    assert sll.get_next(sll.get_node(3)) is sll.null
    assert sll.get_prev(sll.get_node(3)) is sll.get_node(2)
    assert not sll.has_next(sll.null)
    assert sll.get_prev(sll.null) is sll.get_node(3)
    with pytest.raises(IndexError):
        sll.get_node(4)


def test_insert_at_index_one_of_three_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer()
    sll.insert_node(1, 10)

    assert len(sll) == 4
    assert len(sll.values) == 4
    assert len(sll.nodes) == 4
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.tail is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 10
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_node(2).value == 1
    assert sll.get_node_index(sll.get_node(2)) == 2
    assert sll.get_node(3).value == 2
    assert sll.get_node_index(sll.get_node(3)) == 3
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_next(sll.get_node(1)) is sll.get_node(2)
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    assert sll.get_next(sll.get_node(2)) is sll.get_node(3)
    assert sll.get_prev(sll.get_node(2)) is sll.get_node(1)
    assert sll.get_next(sll.get_node(3)) is sll.null
    assert sll.get_prev(sll.get_node(3)) is sll.get_node(2)
    assert not sll.has_next(sll.null)
    assert sll.get_prev(sll.null) is sll.get_node(3)
    with pytest.raises(IndexError):
        sll.get_node(4)


def test_insert_at_index_two_of_three_node_sll() -> None:
    sll = SinglyLinkedList.create_sll(0, 1, 2, color=WHITE).add_null().add_head_pointer().add_tail_pointer()
    sll.insert_node(2, 10)

    assert len(sll) == 4
    assert len(sll.values) == 4
    assert len(sll.nodes) == 4
    assert sll.color == WHITE
    assert sll.has_null is True
    assert sll.has_head is True
    assert sll.has_tail is True
    assert sll.head is not sll.tail
    assert sll.head is not sll.null
    assert sll.tail is not sll.null
    assert sll.has_head_pointer is True
    assert sll.has_tail_pointer is True
    assert sll.head_pointer.pointee is sll.head
    assert sll.tail_pointer.pointee is sll.tail
    assert sll.get_node(0).value == 0
    assert sll.get_node_index(sll.get_node(0)) == 0
    assert sll.get_node(1).value == 1
    assert sll.get_node_index(sll.get_node(1)) == 1
    assert sll.get_node(2).value == 10
    assert sll.get_node_index(sll.get_node(2)) == 2
    assert sll.get_node(3).value == 2
    assert sll.get_node_index(sll.get_node(3)) == 3
    assert sll.get_next(sll.get_node(0)) is sll.get_node(1)
    assert sll.get_prev(sll.get_node(0)) is None
    assert sll.get_next(sll.get_node(1)) is sll.get_node(2)
    assert sll.get_prev(sll.get_node(1)) is sll.get_node(0)
    assert sll.get_next(sll.get_node(2)) is sll.get_node(3)
    assert sll.get_prev(sll.get_node(2)) is sll.get_node(1)
    assert sll.get_next(sll.get_node(3)) is sll.null
    assert sll.get_prev(sll.get_node(3)) is sll.get_node(2)
    assert not sll.has_next(sll.null)
    assert sll.get_prev(sll.null) is sll.get_node(3)
    with pytest.raises(IndexError):
        sll.get_node(4)


def test_add_null_node_to_non_empty_sll() -> None:
    sll = SinglyLinkedList(0, color=WHITE)

    return_value = sll.add_null()

    assert return_value is sll
    assert sll.has_null
    assert sll.has_head
    assert sll.has_tail
    assert sll.head is sll.tail
    assert sll.get_next(sll.tail) is sll.null
    assert not sll.has_next(sll.null)


def test_add_null_node_to_empty_sll() -> None:
    sll = SinglyLinkedList.create_sll(color=WHITE)

    return_value = sll.add_null()

    assert return_value is sll
    assert sll.has_null
    assert sll.has_head
    assert sll.has_tail
    assert sll.head is sll.tail
    assert sll.head is sll.null
    assert not sll.has_next(sll.null)


def test_add_null_node_to_sll_that_already_has_null() -> None:
    sll = SinglyLinkedList.create_sll(color=WHITE).add_null()

    return_value = sll.add_null()

    assert return_value is sll
    assert sll.has_null
    assert sll.has_head
    assert sll.has_tail
    assert sll.head is sll.tail
    assert sll.head is sll.null
    assert not sll.has_next(sll.null)


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


