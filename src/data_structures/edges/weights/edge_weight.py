from __future__ import annotations

from colour import Color

from ...element import Element
from .weight import Weight
from src.constants import DEFAULT_ELEMENT_FONT_SIZE
from src.constants import DEFAULT_MOBJECT_COLOR
from src.custom_vmobject import CustomVMobject


class EdgeWeight(Weight, CustomVMobject):
    def __init__(
        self,
        value: float,
        color: str | Color = DEFAULT_MOBJECT_COLOR,
        font_size: int = DEFAULT_ELEMENT_FONT_SIZE,
    ) -> None:
        super().__init__()
        self._element: Element = Element(
            value=value, color=color, font_size=font_size,
        )

    def __str__(self) -> str:
        return str(self._element)

    def equals(self, other: Weight | float) -> bool:
        if isinstance(other, type(self)):
            return self.value == other.value
        elif isinstance(other, (float, int)):
            return self.value == other
        raise NotImplementedError(
            f'Equality check not implemented between types {type(self)} and {type(other)}',
        )

    @property
    def value(self) -> float:
        return self._element.value

    def get_color(self) -> Color:
        return self._element.color

    def set_color(self, new_color: str | Color) -> None:
        if type(new_color) == str:
            new_color = Color(new_color)

        self._element.color = new_color

    @property
    def font_size(self) -> int:
        return self._element.font_size
