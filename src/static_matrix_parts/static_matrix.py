from manim import *
from colour import Color

from static_array_parts.static_array import StaticArrayBuilder
from typing import Iterable, Tuple

import inspect

class StaticMatrix(VMobject):
    """
    Animation and internal logic for a static matrix
    """
    def __init__(self, num_rows, num_columns):
        super().__init__()
        self._num_rows = num_rows
        self._num_columns = num_columns

    def add_pointer_to_front(self, row: int, column: int, name: str) -> Iterable[Animation]:
        return self._matrix[row].add_pointer_to_front(index=column, name=name)

    def add_pointer_to_back(self, row: int, column: int, name: str) -> Iterable[Animation]:
        return self._matrix[row].add_pointer_to_back(index=column, name=name)

    def remove_pointer(self, name: str) -> Iterable[Animation]:
        for arr in self._matrix:
            if arr.contains_pointer_name(name):
                return arr.remove_pointer(name)
        raise ValueError(f'Can\'t find pointer {name}')

    # TODO: Implement this at the right level of abstraction
    def move_pointer(self, name: str, num_rows: int = 0, num_columns: int = 0) -> Iterable[Animation]:
        from_row_index = self._row_index_of_pointer(name)
        from_row = self._matrix[from_row_index]
        if num_rows == 0:
            return from_row.move_pointer(name=name, num_positions=num_columns)

        from_column_index = from_row.pointers._index_of_pointer(name)
        pointer_to_move = from_row.pointers._cells[from_column_index].get_pointer(name)

        animations = []
        to_row_index = from_row_index + num_rows
        to_row = self._matrix[to_row_index]
        to_column_index = from_row.index_of_pointer(name) + num_columns
        old_pointer_location = pointer_to_move.get_center()
        # Add pointer to front
        if num_rows > 0:
            animations += to_row.add_pointer_to_front(to_column_index, name, arg_pointer=pointer_to_move)
        else:
            animations += to_row.add_pointer_to_back(to_column_index, name, arg_pointer=pointer_to_move)

        to_row.pointers._remove_animation(FadeIn, pointer_to_move, animations)

        from_cell = from_row.pointers._cells[from_row.pointers._index_of_pointer(name)]
        animations += from_cell.remove_pointer(name)
        from_row.pointers._remove_animation(FadeOut, pointer_to_move, animations)
        new_pointer_location = to_row.pointers._cells[to_column_index].get_pointer(name).get_center()

        return animations

    # TODO: Consistency in naming of row and row_index/columns
    def move_pointer_to_row_column(self, name: str, row: int, column: int) -> Iterable[Animation]:
        curr_row = self._row_index_of_pointer(name)
        num_rows = row - curr_row

        curr_column = self._column_index_of_pointer(name)
        num_columns = column - curr_column
        return self.move_pointer(name, num_rows=num_rows, num_columns=num_columns)

    # TODO: Figure out placement of everything
    def set_value_at_row_column(self, value: int, row: int, column: int) -> Iterable[Animation]:
        return self._matrix[row].set_value_at_index(value, column)

    def copy_value_from_index_to_index(self, from_row: int, from_column: int, to_row: int, to_column: int) -> Iterable[Animation]:
        if from_row == to_row:
            return self._matrix[from_row].elements.copy_value_from_index_to_index(from_column, to_column)

        animations = [*self._matrix[to_row].elements._cells[to_column].fade_value()]

        self._matrix[to_row].elements._cells[to_column].set_value(self._matrix[from_row].elements._cells[from_column].get_value().copy())

        self._matrix[to_row].elements._cells[to_column]._value.move_to(self._matrix[from_row].elements._cells[from_column])

        animations.append(self._matrix[to_row].elements._cells[to_column]._value.animate.move_to(self._matrix[to_row].elements._cells[to_column]))
        return animations

    # FIXME: One of the elements being swap snaps to some location before swapping
    def swap(self, row_i: int, column_i: int, row_j: int, column_j: int) -> Iterable[Animation]:
        if row_i == row_j:
            return self._matrix[row_i].swap(column_i, column_j)

        old_i_value = self._matrix[row_i].elements._cells[column_i].get_value()
        old_j_value = self._matrix[row_j].elements._cells[column_j].get_value()

        animations = self._move_element_from_index_to_index(row_j, column_j, row_i, column_i)

        self._matrix[row_i].elements._cells[column_i].set_value(old_i_value)

        animations += self._move_element_from_index_to_index(row_i, column_i, row_j, column_j)

        self._matrix[row_i].elements._cells[column_i].set_value(old_j_value.copy())

        self._matrix[row_i].elements._remove_animation(FadeOut, animations)

        return animations

    def compare(self, *coords: Iterable[Tuple[int]], fn = None, true_color = None, false_color = None) -> Iterable[Animation]:
        if true_color is None: true_color = Color(hue=7/20, saturation=1, luminance=0.5)
        if false_color is None: false_color = Color(hue=0, saturation=1, luminance=0.5)

        if fn is not None:
            return NotImplementedError('Custom comparison function is not implemented')
        values_to_compare = []
        for i, arr in enumerate(self._matrix):
            # Check if arr has elements we want to compare
            for coord in coords:
                if coord[0] == i:
                    values_to_compare.append(arr.elements._cells[coord[1]].get_value().get_value())

        are_equal = len(set(values_to_compare)) == 1

        color = true_color if are_equal else false_color

        animations = []
        for row, column in coords:
            cell = self._matrix[row].elements._cells[column]
            indicate_square = Rectangle(width=cell.width, height=cell.height, stroke_width=0, color=config.background_color, z_index=-1).move_to(cell).set_fill(opacity=0.5)
            animations.append(Indicate(indicate_square, color=color, scale_factor=1))

        return animations


        




    def _row_index_of_pointer(self, name: str) -> int:
        for i, row in enumerate(self._matrix):
            if row.contains_pointer_name(name): return i
        raise ValueError(f'Can\'t find pointer {name}')

    def _column_index_of_pointer(self, name: str) -> int:
        for i, row in enumerate(self._matrix):
            if row.contains_pointer_name(name):
                return row.index_of_pointer(name)
        raise ValueError(f'Can\'t find pointer {name}')

    def _move_element_from_index_to_index(self, from_row: int, from_column: int, to_row: int, to_column: int) -> Iterable[Animation]:
        animations = []
        self._matrix[to_row].elements._cells[to_column].set_value(self._matrix[from_row].elements._cells[from_column].get_value())

        self._matrix[to_row].elements._cells[to_column]._value.move_to(self._matrix[from_row].elements._cells[from_column])

        animations.append(self._matrix[to_row].elements._cells[to_column]._value.animate.move_to(self._matrix[to_row].elements._cells[to_column]))
        return animations
            
            


class StaticMatrixBuilder:
    """
    Builder for a static matrix
    """
    def __init__(self, num_rows = 4, num_columns = 4, descriptors = False, underflow = False, overflow = False, pointers=False):
        self._instance = StaticMatrix(num_rows=num_rows, num_columns=num_columns)
        self._num_rows = num_rows
        self._num_columns = num_columns
        self._has_descriptors = descriptors # This will be used for static matrix specific descriptors
        self._underflow = underflow
        self._overflow = overflow
        self._has_pointers = pointers

    def add_indices(self) -> 'StaticMatrixBuilder':
        '''
        Add indices to animation
        '''
        return self

    def add_elements(self) -> 'StaticMatrixBuilder':
        matrix = []
        for i in range(self._num_rows):
            base_arr_builder = StaticArrayBuilder(length=self._num_columns, descriptors=self._has_descriptors, underflow=self._underflow, overflow=self._overflow).add_elements()

            if self._has_pointers:
                base_arr_builder.add_pointers(stroke_width=1)
            
            matrix.append(base_arr_builder.build())
            if i > 0:
                matrix[i].next_to(matrix[i - 1], DOWN, buff=0)
            self._instance.add(matrix[i])

        self._instance._matrix = matrix

        # for row in self._instance._matrix:
        #     print(id(row))
        return self

    def build(self) -> StaticMatrix:
        '''
        Piece together each component of the StaticMatrix
        '''
        self._instance.move_to([0, 0, 0])
        return self._instance

