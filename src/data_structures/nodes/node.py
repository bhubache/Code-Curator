from __future__ import annotations

from collections.abc import Sequence

from custom_vmobject import CustomVMobject
from data_structures.static_array_parts.values.element import Element


class Node(CustomVMobject):
    def __init__(self, data: float | str, shape: CustomVMobject):
        super().__init__(color='#DBC9B8')
        self._radius: float = 0.5
        self._stroke_width: int = 2
        self._shape: CustomVMobject = shape
        self._data: Element = Element(data)
        self._container = self._shape(
            radius=self._radius, stroke_width=self._stroke_width, color=self.color,
        )
        self._container.add(self._data)
        self.add(self._container)

    def data_equals(self, value) -> bool:
        return self._data._value == value

    @property
    def data(self):
        return self._data._value

    def get_container_center(self) -> Sequence[float]:
        return self._container.get_center()

    def get_container_top(self) -> Sequence[float]:
        return self._container.get_top()

    def get_container_right(self) -> Sequence[float]:
        return self._container.get_right()

    def get_container_bottom(self) -> Sequence[float]:
        return self._container.get_bottom()

    def get_container_left(self) -> Sequence[float]:
        return self._container.get_left()

    @property
    def container(self):
        return self._container
