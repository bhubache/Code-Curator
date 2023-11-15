from __future__ import annotations

from manim import ORIGIN

from code_curator.custom_vmobject import CustomVMobject
from code_curator.data_structures.graph import Graph
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

        self.add(self.graph)
        self.move_to(ORIGIN)
