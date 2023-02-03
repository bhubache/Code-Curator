from manim import *

from ..rows.row import Row
from ..cells.index_cell import IndexCell

class IndexRow(Row):
    """
    Animation and internal logic for a row of indices
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_cells(self._create_init_values())
        self._add_cells_to_mobject()

    def _create_init_values(self):
        '''
        Create the intial list of values
        '''
        values = []
        for val in self._range_list:
            values.append(IndexCell(val))
        if self._overflow: values[-1] = IndexCell('length')
        return values


class IndexRowBuilder:
    """
    Builder for a row of indices
    """
    def __init__(self):
        self._instance = None

    def __call__(self, **kwargs):
        self._instance = IndexRow(**kwargs)
        return self._instance
