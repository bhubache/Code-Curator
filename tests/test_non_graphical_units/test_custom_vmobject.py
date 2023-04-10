from __future__ import annotations

import pytest
from manim import Circle
from manim import Line
from manim import Square

from src.custom_vmobject import CustomVMobject
from src.null_vmobject import NullVMobject


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
        Line(), NullVMobject(), Square(),
        NullVMobject(), NullVMobject(),
    )
    assert len(parent.submobjects) == 2
