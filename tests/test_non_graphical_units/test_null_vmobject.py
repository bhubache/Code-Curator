from __future__ import annotations

import pytest
from custom_vmobject import CustomVMobject
from null_vmobject import NullVMobject


@pytest.fixture
def null_vmobject() -> NullVMobject:
    return NullVMobject()


def test_dunder_call(null_vmobject: NullVMobject) -> None:
    assert null_vmobject() == null_vmobject


def test_dunder_get_attr(null_vmobject: NullVMobject) -> None:
    assert null_vmobject.some_attr is None


def test_add_null_vmobject_to_vmobject(null_vmobject: NullVMobject) -> None:
    custom_vmobject: CustomVMobject = CustomVMobject()
    custom_vmobject.add(null_vmobject)
    assert len(custom_vmobject.submobjects) == 0
