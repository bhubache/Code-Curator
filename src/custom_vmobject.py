from __future__ import annotations

from manim import VMobject
from null_vmobject import NullVMobject


class CustomVMobject(VMobject):
    def __init__(self) -> None:
        super().__init__()

    def add(self, *mobjects: VMobject):
        non_null_vmobjects: list[VMobject] = []
        for mob in mobjects:
            if not isinstance(mob, NullVMobject):
                non_null_vmobjects.append(mob)
        super().add(non_null_vmobjects)
