from __future__ import annotations


from ..values.index import Index
from .cell import Cell


class IndexCell(Cell):
    def __init__(self, value):
        super().__init__(Index(value), height=0.5)
