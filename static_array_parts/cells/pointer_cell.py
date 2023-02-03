from manim import *

from .cell import Cell
# from ..values.pointer_sequence import PointerSequence

from ..values.pointer import Pointer
from ..values.pointer_barrier import PointerBarrier

# TODO: Refactor this to not inherit from Cell?

class PointerCell(Cell):
    def __init__(self, value = '', stroke_width = 1):
        # super().__init__(Tex(''), height=0.5, stroke_width=stroke_width)
        super().__init__(Tex(''), height=0.25, stroke_width=stroke_width)
        self._pointers = []
        self._barriers = []

    def add_pointer_to_front(self, pointer):
        if not isinstance(pointer, Pointer):
            raise ValueError('pointer must be of type Pointer: not {type(pointer)}')
        return self._add_pointer_at_index(pointer, 0)

    def add_pointer_to_back(self, pointer):
        if not isinstance(pointer, Pointer):
            raise ValueError('pointer must be of type Pointer: not {type(pointer)}')
        return self._add_pointer_at_index(pointer, len(self._pointers))

    def remove_pointer(self, name):
        pointer_to_remove = self.get_pointer(name)
        animations = self._remove_pointer(pointer_to_remove)
        if self._barriers_present():
            animations += self._remove_barrier(pointer_to_remove)
        return animations

    def _add_pointer_at_index(self, pointer, index):
        if not hasattr(pointer, 'exists'):
            pointer.new = True
        else:
            delattr(pointer, 'exists')
        self._pointers.insert(index, pointer)
        self._relink_barriers()

        animations = []
        if self._new_barrier_needed():
            self._add_barrier_internal(pointer, index)
            if index == len(self._barriers):
                index -= 1
            animations.append(FadeIn(self._barriers[index]))
            self._barriers[index].new = True

        animations.append(FadeIn(pointer))
        animations += self._distribute_elements()
        # self._relink_barriers()

        return animations

    def _distribute_elements(self):
        num_pointers = len(self._pointers)
        num_barriers = len(self._barriers)

        space = self.width / (num_pointers + num_barriers + 1)
        starting_location = self.get_left()

        animations = []
        for i in range(num_pointers):
            if not hasattr(self._pointers[i], 'new'):
                animations.append(self._pointers[i].animate.move_to(starting_location + [space * ((i * 2) + 1), 0, 0]))
            else:
                self._pointers[i].move_to(starting_location + [space * ((i * 2) + 1), 0, 0])
                delattr(self._pointers[i], 'new')


        for i in range(num_barriers):
            barrier_start = [0, 0, 0]
            barrier_end = [0, 0, 0]

            barrier_start[0] = starting_location[0] + (space * ((i + 1) * 2))
            barrier_start[1] = self.get_top()[1]
            barrier_start[2] = starting_location[2]

            barrier_end[0] = barrier_start[0]
            barrier_end[1] = self.get_bottom()[1]
            barrier_end[2] = barrier_start[2]
            if not hasattr(self._barriers[i], 'new'):
                animations.append(self._barriers[i].animate.put_start_and_end_on(barrier_start, barrier_end))
            else:
                self._barriers[i].put_start_and_end_on(barrier_start, barrier_end)
                delattr(self._barriers[i], 'new')

        return animations


    def _add_pointer_internal(self, name, index):
        pointer = Pointer(name).move_to(self)
        pointer.new = True
        self._pointers.insert(index, pointer)

        if len(self._pointers) > 1:
            self._barriers.insert(index, PointerBarrier(pointer_name=pointer.get_value()))

            # self._add_barrier_internal(pointer, index)
            # self._barriers.insert(index, PointerBarrier(pointer))
            if index == len(self._barriers):
                index -= 1
            animations.append(FadeIn(self._barriers[index]))
            self._barriers[index].new = True

    def _add_barrier_internal(self, pointer, index):
        self._barriers.insert(index, PointerBarrier(pointer_name=pointer.get_value()))
        self._relink_barriers()

    def get_pointer(self, name):
        for pointer in self._pointers:
            if str(pointer) == name: return pointer
        return None

    def _remove_pointer(self, pointer):
        self._pointers.remove(pointer)

        animations = []
        animations.append(FadeOut(pointer))
        return animations

    def _remove_barrier(self, pointer):
        barrier_to_remove = self._get_barrier(pointer)
        self._barriers.remove(barrier_to_remove)
        self._relink_barriers()

        animations = []
        animations.append(FadeOut(barrier_to_remove))
        animations += self._distribute_elements()
        return animations

    def _relink_barriers(self):
        if self._barriers_present():
            for pointer, barrier in zip(self._pointers, self._barriers):
                barrier.link_to_pointer(pointer)
            self._barriers[-1].link_to_pointer(self._pointers[-1])
            

    def _get_barrier(self, pointer):
        for i, barrier in enumerate(self._barriers):
            if barrier.is_linked_to_pointer(pointer): return barrier
        raise Exception(f'Can\'t find barrier associated with pointer {pointer}')

    def contains_pointer_name(self, name):
        find_pointer = Pointer(name)
        for pointer in self._pointers:
            if pointer == find_pointer: return True
        return False

    def _barriers_present(self):
        return len(self._barriers) > 0

    def _new_barrier_needed(self):
        return len(self._pointers) - len(self._barriers) >= 2