from manim import *

from .cell import Cell
from ..values.element import Element

class ElementCell(Cell):
    def __init__(self, value, index):
        self.element = Element(value)
        self.index = index
        super().__init__(Element(value))

    '''
    This commented out code screws up the ElementRow, making it such that
    only one seems to be able to exist at a time. Therefore, it screws up
    StaticMatrix because it has multiple ElementRows in it. I thought this
    code was the solution to an early problem, but I suppose it wasn't..
    however, the code still works sooooo this may have been on the path to
    the actual solution.
    '''
    # def __key(self):
    #     return (self.index)

    # def __hash__(self):
    #     return hash(self.__key())

    # def __eq__(self, other):
    #     if isinstance(other, type(self)):
    #         return self.__key() == other.__key()
    #     return NotImplemented

    # def __str__(self):
    #     '''
    #     Tex('i')
    #     '''
    #     return str(self.element)

    def add_value(self, value):
        element = Element(value)
        element.move_to(self.get_center())
        animations = [FadeIn(element)]
        return animations

    def set_value(self, element):
        # NOTE: FOR SOME REASON, SELF.REMOVE MAKES THIS ANIMATION WORK!
        self.remove(self._value)

        new_value = element.move_to(self.get_center())
        animations = [ReplacementTransform(self._value, new_value)]
        self._value = new_value
        return animations

    def fade_value(self):
        '''
        Fade's out value from screen
        '''
        return [FadeOut(self._value)]

    def get_value(self):
        return self._value

    # FIXME: Hopefully temporary until I can get animatino to work with
    # __hash__ for Value to be dependent on the actual primitive value
    def get_primitive_value(self):
        return self._value._value

