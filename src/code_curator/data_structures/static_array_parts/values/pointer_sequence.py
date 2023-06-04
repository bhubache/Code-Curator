from __future__ import annotations

from manim import *

from .pointer import Pointer
from .pointer_barrier import PointerBarrier


class PointerSequence(Rectangle):
    def __init__(self, color='#DBC9B8'):
        super().__init__(color=color, width=0, height=0)
        self.set_opacity(0)
        self._pointers = []
        self._barriers = []

    def add_pointer(self, name):
        pointer = Pointer(name).move_to(self)
        self._pointers.insert(0, pointer)

        if len(self._pointers) > 1:
            self._barriers.append(
                PointerBarrier(
                pointer, start=[0, 0, 0], end=[0, 0 - self.height, 0],
                ),
            )

        self._distribute_elements()

        return [FadeIn(pointer)]

    def _distribute_elements(self):
        num_pointers = len(self._pointers)
        num_barriers = len(self._barriers)

        space = self.width / (num_pointers + num_barriers + 1)
        starting_location = self.get_left()
        for i in range(num_pointers):
            self.get_pointer_at_index(i).move_to(
                starting_location + [space * ((i * 2) + 1), 0, 0],
            )
            self.add(self.get_pointer_at_index(i))

        for i in range(num_barriers):
            barrier_start = [0, 0, 0]
            barrier_end = [0, 0, 0]

            barrier_start[0] = starting_location[0] + (space * ((i + 1) * 2))
            barrier_start[1] = self.get_top()[1]
            barrier_start[2] = starting_location[2]

            barrier_end[0] = barrier_start[0]
            barrier_end[1] = self.get_bottom()[1]
            barrier_end[2] = barrier_start[2]
            self.barriers[i].put_start_and_end_on(barrier_start, barrier_end)
            self.add(self.get_barrier_at_index(i))

    def _add_barrier(self, pointer):
        self._pointer_barriers.insert(
            0, PointerBarrier(name=pointer.get_value()),
        )
