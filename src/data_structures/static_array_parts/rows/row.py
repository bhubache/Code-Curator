from manim import *

from ..cells.cell import Cell
from ..values.value import Value

from typing import Iterable

class Row(VMobject):
    """
    Base class for all row types
    """
    def __init__(self, length, underflow, overflow, **_ignored):
        super().__init__()
        self._cells = {}
        self._length = length
        self._underflow = underflow
        self._overflow = overflow
        self._display_length = self._length + int(underflow) + int(overflow)
        self._range_list = [i for i in range((0 - int(underflow)), self._length + int(overflow))]

    def __getitem__(self, index: int) -> Cell:
        return self._cells[index]

    def _init_cells(self, values: Iterable[Value]):
        for key, value in zip(self._range_list, values):
            self._cells[key] = value

    def _add_cells_to_mobject(self):
        '''
        Add to and position the cells in the row
        so they will be displayed on the screen
        '''
        for key in self._range_list:
            if key > self._range_list[0]:
                self._cells[key].next_to(self._cells[key - 1], RIGHT, buff=0)

            self.add(self._cells[key])

    def get_cells(self) -> Iterable[Cell]:
        '''
        Return unmodifiable view of cells list
        '''
        return self._cells.copy()

    def set_cell(self, index: int, cell: Cell):
        self._cells[index] = cell