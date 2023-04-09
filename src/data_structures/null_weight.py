from __future__ import annotations

from null_vmobject import NullVMobject

from .weight import Weight


class NullWeight(NullVMobject, Weight):
    def __init__(self) -> None:
        pass

    def __call__(self, *args, **kwargs):
        return self
