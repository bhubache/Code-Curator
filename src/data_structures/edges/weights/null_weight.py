from __future__ import annotations

from .weight import Weight
from src.null_vmobject import NullVMobject


class NullWeight(NullVMobject, Weight):
    @property
    def value(self) -> None:
        return None
