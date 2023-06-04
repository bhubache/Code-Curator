from __future__ import annotations

from manim import *


class PointerBarrier(Line):
    def __init__(self, pointer_name):
        super().__init__(color='#DBC9B8', stroke_width=1)
        self._ids = [pointer_name]

    def is_linked_to_pointer(self, pointer):
        return pointer.name in self._ids

    def link_to_pointer(self, pointer):
        self._ids.append(pointer.name)
