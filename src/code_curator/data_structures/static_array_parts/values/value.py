from __future__ import annotations


from manim import *

# NOTE: While it makes sense for the identify of a value to be solely dependent on
# it's value (5 is the same as any other 5), I don't think it makes sense for animation
# if I want to have an array where multiple cells have the same value, they need to be
# different mobjects. So, I'm making the hash the id of the instance of value


class Value(Tex):
    """
    Base class for cell values
    """

    def __init__(self, value):
        self._value = value
        super().__init__(value, color='#DBC9B8')
        self.font_size = 17

    def __key(self):
        # return (self._value, )
        return (id(self),)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.__key() == other.__key()
        return NotImplemented

    def equals(self, other):
        return self._value == other._value

    def __str__(self):
        '''
        Tex('i')
        '''
        return str(self._value)

    def get_value(self):
        return self._value
