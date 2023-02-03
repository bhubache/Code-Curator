from manim import *
from .value import Value


class Pointer(Value):
    """
    Tex mobject for a cell's pointer(s)
    """
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise ValueError(f'A Pointer can only be passed a str: given type {type(name)}')
        super().__init__(name)

    def __key(self):
        return (self._value, )

    def __hash__(self):
        return hash(self.__key())    

    def __eq__(self, other):
        if isinstance(other, Pointer):
            return self.__key() == other.__key()
        return NotImplemented


    # def get_value(self):
    #     return super().value

    # @property
    # def value(self):
    #     return super().value