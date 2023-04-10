from __future__ import annotations

from typing import Any

from manim import VMobject


class NullVMobject(VMobject):
    def __init__(self) -> None:
        pass

    def __call__(self, *args: Any, **kwargs: Any) -> NullVMobject:
        return self

    def __getattr__(self, attr: Any) -> None:
        return None
