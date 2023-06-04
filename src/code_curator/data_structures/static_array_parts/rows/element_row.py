from manim import *
from colour import Color

from static_array_parts.rows.row import Row
from ..cells.element_cell import ElementCell
from ..values.element import Element

from typing import Iterable

class ElementRow(Row):
    """
    Animation and internal logic for a row of elements
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_cells(self._create_init_values())
        self._add_cells_to_mobject()

    def _create_init_values(self) -> Iterable[ElementCell]:
        '''
        Create the intial list of values
        '''
        values = []
        if self._underflow: values.append(ElementCell('-', -1))
        for i in range(self._length):
            values.append(ElementCell(0, i))
        if self._overflow: values.append(ElementCell('-', self._length))
        return values

    def set_value_at_index(self, value: int, index: int) -> Iterable[Animation]:
        element = Element(value)
        return self._cells[index].set_value(element)

    def copy_value_from_index_to_index(self, from_index: int, to_index: int) -> Iterable[Animation]:
        animations = [*self._cells[to_index].fade_value()]

        # This method returns animations, but we only care about the internal logic
        # We pass in a copy because we don't want to manipulate the internals
        # of the from_index cell
        self._cells[to_index].set_value(self._cells[from_index].get_value().copy())

        self._cells[to_index]._value.move_to(self._cells[from_index])

        animations.append(self._cells[to_index]._value.animate.move_to(self._cells[to_index]))
        return animations

    def swap(self, i: int, j: int) -> Iterable[Animation]:
        old_i_value = self._cells[i].get_value()
        old_j_value = self._cells[j].get_value()

        animations = self._move_element_from_index_to_index(j, i)

        # We need to set the internal value at i back to what it was for the next aniamtion
        # to proceed successfully
        # self.set_value_at_index(old_i_value, i)
        self._cells[i].set_value(old_i_value)

        animations += self._move_element_from_index_to_index(i, j)

        # Now we need to fix the internal data by setting the value at i to what it's suppposed to be
        # self.set_value_at_index(old_j_value, i)
        self._cells[i].set_value(old_j_value.copy())

        self._remove_animation(FadeOut, animations)

        return animations

    # FIXME: Some strange thing where an Element's value is another Element object.
    # Probably from the swap method
    def compare(self, *indices: Iterable[int], fn = None, true_color = None, false_color = None) -> Iterable[Animation]:
        if true_color is None: true_color = Color(hue=7/20, saturation=1, luminance=0.5)
        if false_color is None: false_color = Color(hue=0, saturation=1, luminance=0.5)

        if fn is not None:
            return NotImplementedError('Custom comparison function is not implemented')

        cells_to_compare = [cell.get_value() for i, cell in self._cells.items() if i in indices]
        values_to_compare = [e.get_value() for e in cells_to_compare]

        are_equal = len(set(values_to_compare)) == 1

        color = true_color if are_equal else false_color

        animations = []
        for index in indices:
            cell = self._cells[index]
            indicate_square = Rectangle(width=cell.width, height=cell.height, stroke_width=0, color=config.background_color, z_index=-1).move_to(cell).set_fill(opacity=0.5)
            animations.append(Indicate(indicate_square, color=color, scale_factor=1))

        return animations

    def _move_element_from_index_to_index(self, from_index: int, to_index: int) -> Iterable[Animation]:
        animations = []
        # This method returns animations, but we only care about the internal logic
        # We pass in a copy because we don't want to manipulate the internals
        # of the from_index cell
        self._cells[to_index].set_value(self._cells[from_index].get_value())

        self._cells[to_index]._value.move_to(self._cells[from_index])

        animations.append(self._cells[to_index]._value.animate.move_to(self._cells[to_index]))
        return animations

    def _remove_animation(self, animation_type: type(Animation), animations: Iterable[Animation]):
        for animation in animations:
            if isinstance(animation, animation_type):
                animations.remove(animation)

    
class ElementRowBuilder:
    """
    Builder for a row of elements
    """
    def __init__(self):
        self._instance = None

    def __call__(self, **kwargs):
        self._instance = ElementRow(**kwargs)
        return self._instance
