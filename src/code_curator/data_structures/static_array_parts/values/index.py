from __future__ import annotations


from ..values.value import Value

# TODO: Index values must be unique for a given array


class Index(Value):
    """
    Tex mobject for a cell's index
    """

    def __init__(self, index: int):
        # if not isinstance(index, int):
        #     raise ValueError(f'An Index can only be passed an integer: given type {type(index)}')
        super().__init__(index)

    # @property
    # def value(self):
    #     return super().value
