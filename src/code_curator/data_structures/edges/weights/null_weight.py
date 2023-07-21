from __future__ import annotations

from code_curator.null_vmobject import NullVMobject

from .weight import Weight


class NullWeight(NullVMobject, Weight):
    @property
    def value(self) -> None:
        return None