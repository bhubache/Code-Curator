from __future__ import annotations

from manim import DOWN
from manim import ORIGIN

from code_curator.custom_vmobject import CustomVMobject
from code_curator.data_structures.graph import Graph
from code_curator.data_structures.graph import LabeledLine
from code_curator.data_structures.graph import Vertex


class SinglyLinkedList(CustomVMobject):
    def __init__(self, *values) -> None:
        super().__init__()
        self.values = values
        self.graph = Graph()

        for index, value in enumerate(self.values):
            vertex = Vertex(
                contents=value,
                show_label=False,
                position=(index, 0.0, 0.0),
            )
            self.graph.add_vertex(vertex)

        for index in range(len(self.values) - 1):
            curr_node = self.graph.get_vertex(f"Label{index}")
            next_node = self.graph.get_vertex(f"Label{index + 1}")

            self.graph.add_edge(curr_node, next_node, directedness="->")

        self.head_pointer = LabeledLine(self.graph.get_vertex("Label0"), label="head", direction=DOWN)
        self.tail_pointer = LabeledLine(
            self.graph.get_vertex(f"Label{len(self.values) - 1}"),
            label="tail",
            direction=DOWN,
        )

        self.add(self.graph)
        self.add(self.head_pointer)
        self.add(self.tail_pointer)
        self.move_to(ORIGIN)
