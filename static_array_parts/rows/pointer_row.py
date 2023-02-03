from manim import *

from static_array_parts.rows.row import Row
from ..cells.pointer_cell import PointerCell
from ..values.pointer import Pointer

class PointerRow(Row):
    """
    Animation and internal logic for a row of pointers
    """
    def __init__(self, stroke_width, **kwargs):
        super().__init__(**kwargs)
        self._init_cells([PointerCell(stroke_width=stroke_width) for _ in self._range_list])
        self._add_cells_to_mobject()

    def add_pointer_to_front(self, index, name, arg_pointer = None):
        pointer = Pointer(name)
        if self._contains_pointer_name(name):
            pointer = self._get_pointer(name)
            pointer.exists = True
        if arg_pointer is not None:
            pointer = arg_pointer
            pointer.exists = True
        return self[index].add_pointer_to_front(pointer)

    def add_pointer_to_back(self, index, name, arg_pointer = None):
        pointer = Pointer(name)
        if self._contains_pointer_name(name):
            pointer = self._get_pointer(name)
            pointer.exists = True
        if arg_pointer is not None:
            pointer = arg_pointer
            pointer.exists = True
        return self[index].add_pointer_to_back(pointer)

    def remove_pointer(self, name):
        if not self._contains_pointer_name(name):
            raise RunTimeError(f'pointer name: {name} not found')
        
        cell = self._cells[self._index_of_pointer(name)]
        return cell.remove_pointer(name)

    def move_pointer(self, name, num_positions):
        if not self._contains_pointer_name(name):
            raise ValueError('Unable to find pointer {name}')

        from_index = self._index_of_pointer(name)
        from_cell = self._cells[from_index]

        to_index = from_index + num_positions
        assert self.index_in_bounds(to_index), 'to index {to_index} out of bounds'
        to_cell = self._cells[self._index_of_pointer(name) + num_positions]

        pointer_to_move = from_cell.get_pointer(name)
        print(id(pointer_to_move))
        animations = []

        # Create animations for and internally add pointer to new cell
        if from_index < to_index:
            animations += self.add_pointer_to_front(to_index, name)
        else:
            animations += self.add_pointer_to_back(to_index, name)
        self._remove_animation(FadeIn, pointer_to_move, animations)

        animations += from_cell.remove_pointer(name)
        self._remove_animation(FadeOut, pointer_to_move, animations)
        return animations

    def move_pointer_to_index(self, name, to_index):
        if not self._contains_pointer_name(name):
            raise ValueError('Unable to find pointer {name}')
        assert self.index_in_bounds(to_index), 'to index {to_index} out of bounds'

        from_index = self._index_of_pointer(name)
        return self.move_pointer(name, to_index - from_index)
        

    def _remove_animation(self, animation_type, pointer, animations):
        for animation in animations:
            if isinstance(animation, animation_type) and animation.mobject == pointer:
                animations.remove(animation)
                break

    def _index_of_pointer(self, name):
        for i, cell in self._cells.items():
            if cell.contains_pointer_name(name): return i
        return -1

    def _contains_pointer_name(self, name):
        for cell in self._cells.values():
            if cell.contains_pointer_name(name): return True
        return False

    def _get_pointer(self, name):
        for cell in self._cells.values():
            if cell.contains_pointer_name(name): return cell.get_pointer(name)
        return None

    def index_in_bounds(self, index):
        return index >= self._range_list[0] and index <= self._range_list[-1]


class PointerRowBuilder:
    """
    Builder for a row of pointers
    """
    def __init__(self):
        self._instance = None

    def __call__(self, **kwargs):
        self._instance = PointerRow(**kwargs)
        return self._instance

