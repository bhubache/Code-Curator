from manim import VMobject, Animation, LEFT, DOWN

from static_array_parts.rows.row_factory import RowFactory
from static_array_parts.rows.index_row import IndexRowBuilder
from static_array_parts.rows.element_row import ElementRowBuilder
from static_array_parts.rows.pointer_row import PointerRowBuilder

from static_array_parts.values.pointer import Pointer

from static_array_parts.cells.cell import Cell
from static_array_parts.rows.row import Row

from typing import Iterable

'''
    TODO:
    - Add ability to change stroke_width of just top line of pointer cell
    - Separate view and model logic!!!
    - Clean up StaticArrayBuilder
        - I don't like how the build method is implemented
        - I don't like how the description cells are created
    - Understand properties so code is more pythonic
    - Decide (with good reason) when primitives should be converted to their Value type
'''

def validate_arguments(fn):
    '''
    Decorator for validating the positional and keyword arguments of a method
    '''
    def inner(obj, *args, **kwargs):
        annotations = fn.__annotations__

        for (arg, type_) in zip(args, annotations):
            assert isinstance(arg, annotations[type_]), \
                f'arg {arg} is of type {type(arg)}, should be {annotations[type_]}'

        for arg in kwargs:
            assert isinstance(kwargs[arg], annotations[arg]), \
                f'arg {arg} is of type {type(arg)}, should be {annotations[arg]}'

        result = fn(obj, *args, **kwargs)

        return result
    return inner

class StaticArray(VMobject):
    """
    Animation and internal logic for a static array
    """
    def __init__(self, length):
        super().__init__()
        self._length = length

    # def __key(self):
    #     return id(self)

    # def __hash__(self):
    #     return hash(self.__key())

    # def __eq__(self, other):
    #     if isinstance(other, type(self)):
    #         return self.__key() == other.__key()
    #     return NotImplemented


    @validate_arguments
    def add_pointer_to_front(self, index: int, name: str, arg_pointer: Pointer = None) -> Iterable[Animation]:
        return self.pointers.add_pointer_to_front(index, name, arg_pointer)

    @validate_arguments
    def add_pointer_to_back(self, index: int, name: str, arg_pointer: Pointer = None) -> Iterable[Animation]:
        return self.pointers.add_pointer_to_back(index, name, arg_pointer)

    @validate_arguments
    def remove_pointer(self, name: str) -> Iterable[Animation]:
        return self.pointers.remove_pointer(name)

    @validate_arguments
    def move_pointer(self, name: str, num_positions: int) -> Iterable[Animation]:
        return self.pointers.move_pointer(name, num_positions)

    @validate_arguments
    def move_pointer_to_index(self, name: str, index: int) -> Iterable[Animation]:
        return self.pointers.move_pointer_to_index(name, index)

    @validate_arguments
    def set_value_at_index(self, value: int, index: int) -> Iterable[Animation]:
        return self.elements.set_value_at_index(value, index)

    @validate_arguments
    def copy_value_from_index_to_index(self, from_index: int, to_index: int) -> Iterable[Animation]:
        return self.elements.copy_value_from_index_to_index(from_index, to_index)

    @validate_arguments
    def swap(self, i: int, j: int) -> Iterable[Animation]:
        return self.elements.swap(i, j)

    @validate_arguments
    def compare(self, i: int, j: int) -> Iterable[Animation]:
        return self.elements.compare(i, j)


    # NOTE: Extends too far reaching into pointer row
    def contains_pointer_name(self, name):
        return self.pointers._contains_pointer_name(name)

    # NOTE: Extends too far reaching into pointer row
    def index_of_pointer(self, name):
        return self.pointers._index_of_pointer(name)

    # NOTE: Extends too far reaching into pointer row
    def pointer_index_in_bounds(self, index):
        return self.pointers.index_in_bounds(index)


class StaticArrayBuilder:
    """
    Builder for a static array
    """
    def __init__(self, length = 5, descriptors = False, underflow = False, overflow = False):
        self._instance = StaticArray(length)
        self._has_descriptors = descriptors
        self._underflow = underflow
        self._overflow = overflow

        self.row_factory = RowFactory()
        self.row_factory.register_builder('indices', IndexRowBuilder())
        self.row_factory.register_builder('elements', ElementRowBuilder())
        self.row_factory.register_builder('pointers', PointerRowBuilder())

        self.config = {}
        self.config['length'] = length
        self.config['underflow'] = underflow
        self.config['overflow'] = overflow

    # def add_representation(self) -> 'StaticArrayBuilder':
    #     '''
    #     Add representation row to animation
    #     '''

    def add_indices(self) -> 'StaticArrayBuilder':
        '''
        Add indices row to animation
        '''
        self._instance.indices = self.row_factory.create('indices', **self.config)
        if self._has_descriptors:
            self._instance.index_desc = self.create_index_desc_cell()
        return self

    def add_elements(self) -> 'StaticArrayBuilder':
        '''
        Add elements row to animation
        '''
        self._instance.elements = self.row_factory.create('elements', **self.config)
        if self._has_descriptors:
            self._instance.element_desc = self.create_element_desc_cell()
        return self

    def add_pointers(self, stroke_width=1) -> 'StaticArrayBuilder':
        '''
        Add pointers row to animation
        '''
        self.config['stroke_width'] = stroke_width
        self._instance.pointers = self.row_factory.create('pointers', **self.config)
        if self._has_descriptors:
            self._instance.pointer_desc = self.create_pointer_desc_cell()
        return self

    def build(self) -> StaticArray:
        '''
        Piece together each component of the StaticArray
        '''
        rows_in_scene = []
        if hasattr(self._instance, 'indices'):
            rows_in_scene.append(self._instance.indices)
            self._instance.add(self._instance.indices)
            if self._has_descriptors:
                self.place_desc_cell(self._instance.index_desc, self._instance.indices)
        if hasattr(self._instance, 'elements'):
            if len(rows_in_scene) > 0:
                self._instance.elements.next_to(rows_in_scene[-1], DOWN, buff=0)
            rows_in_scene.append(self._instance.elements)
            self._instance.add(self._instance.elements)
            if self._has_descriptors:
                self.place_desc_cell(self._instance.element_desc, self._instance.elements)
        if hasattr(self._instance, 'pointers'):
            if len(rows_in_scene) > 0:
                self._instance.pointers.next_to(rows_in_scene[-1], DOWN, buff=-0.25)
                # self._instance.pointers.next_to(rows_in_scene[-1], DOWN, buff=0)
            rows_in_scene.append(self._instance.pointers)
            self._instance.add(self._instance.pointers)
            if self._has_descriptors:
                self.place_desc_cell(self._instance.pointer_desc, self._instance.pointers)

        self._instance.move_to([0, 0, 0])
        return self._instance

    def create_index_desc_cell(self) -> Cell:
        index_desc = Cell('indices', height = 0.5)
        return index_desc

    def create_element_desc_cell(self) -> Cell:
        element_desc = Cell('elements')
        return element_desc

    def create_pointer_desc_cell(self) -> Cell:
        pointer_desc = Cell('pointers', height = 0.5)
        return pointer_desc

    def place_desc_cell(self, desc_cell: Cell, row: Row):
        desc_cell.next_to(row, LEFT, buff=0)
        self._instance.add(desc_cell)


