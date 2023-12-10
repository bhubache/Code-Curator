from __future__ import annotations

import numpy as np
import pytest
from manim import Circle
from manim import Line
from manim import Square

from code_curator.custom_vmobject import CustomVMobject
from code_curator.null_vmobject import NullVMobject


@pytest.fixture
def parent() -> CustomVMobject:
    return CustomVMobject()


def test_default_submobjects(parent: CustomVMobject) -> None:
    assert len(parent.submobjects) == 0


def test_add_only_non_null_vmobjects(parent: CustomVMobject) -> None:
    parent.add(Line(), Circle(), Square())
    assert len(parent.submobjects) == 3


def test_add_only_null_vmobjects(parent: CustomVMobject) -> None:
    parent.add(NullVMobject(), NullVMobject(), NullVMobject())
    assert len(parent.submobjects) == 0


def test_add_both_null_and_non_null_vmobjects(parent: CustomVMobject) -> None:
    parent.add(
        Line(),
        NullVMobject(),
        Square(),
        NullVMobject(),
        NullVMobject(),
    )
    assert len(parent.submobjects) == 2


def test_center_with_quasi_add(parent: CustomVMobject) -> None:
    center_before_quasi_add = parent.get_center()
    parent.quasi_add(Circle().move_to((2.0, 2.0, 0.0)))

    assert np.array_equal(center_before_quasi_add, parent.get_center())


def test_center_with_normal_add(parent: CustomVMobject) -> None:
    first_mob = Circle().move_to((2.0, 2.0, 0.0))

    parent_center_before_add = parent.get_center()
    parent.add(first_mob)

    assert not np.array_equal(parent_center_before_add, parent.get_center())


def test_center_with_quasi_add_and_normal_add(parent: CustomVMobject) -> None:
    non_quasi_mob = Circle()
    quasi_mob = non_quasi_mob.copy().move_to((2.0, 2.0, 0.0))

    parent.add(non_quasi_mob)
    parent_center_before_quasi_add = parent.get_center()
    parent.quasi_add(quasi_mob)

    assert np.array_equal(parent_center_before_quasi_add, parent.get_center())
