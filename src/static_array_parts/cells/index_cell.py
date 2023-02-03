from manim import *

from .cell import Cell
from ..values.index import Index

class IndexCell(Cell):
    def __init__(self, value):
        super().__init__(Index(value), height=0.5)