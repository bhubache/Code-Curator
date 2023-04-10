from __future__ import annotations

from typing import Any

from colour import Color
from manim import Tex


class Element(Tex):
    def __init__(
        self,
        value: Any,
        color: str | Color,
        font_size: int,
    ) -> None:
        super().__init__(value, color=color, font_size=font_size)
        self._value: Any = value

    def equals(self, other: Element) -> bool:
        return self._value == other._value

    def __str__(self) -> str:
        '''
        Tex('i')
        '''
        return str(self._value)

    @property
    def value(self) -> Any:
        return self._value
