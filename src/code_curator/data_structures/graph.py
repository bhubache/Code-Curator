from __future__ import annotations

from manim import BLUE_D
from manim import config
from manim import Circle
from manim import ArcBetweenPoints
from manim import DashedLine
from manim import GRAY
from manim import Line
from manim import PI
from manim import RED
from manim import Scene
from manim import UP
from manim import DOWN
from manim import VMobject
from manim import GOLD

from code_curator.constants import DEFAULT_ELEMENT_FONT_SIZE
from code_curator.custom_vmobject import CustomVMobject
from code_curator.data_structures.element import Element
from code_curator.manim_property import manim_property


NODE_WHITE = "#FFFFFF"
NODE_GRAY = "gray"
NODE_BLACK = "black"


class Vertex(CustomVMobject):
    def __init__(self, value, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.predecessor = None
        self.value = Element("", color="#000000")
        self.container = Circle(radius=0.2, color="black", stroke_width=0.75)
        # self.container.add(self.value)
        self.add(self.container)
        self.move_to([self.x, self.y, 0])
        self.add(self.value)
        self.value.move_to(self.container)

        self.label = Element(value, color="#000000", font_size=DEFAULT_ELEMENT_FONT_SIZE - 2)
        self.add(self.label)
        if value == "u" or value == "v" or value == "w":
            self.label.next_to(self.container, UP, buff=0.1)
        else:
            self.label.next_to(self.container, DOWN, buff=0.1)

    def __repr__(self) -> str:
        return f"Vertex({self.value.value})"

    def __str__(self) -> str:
        return self.value.value

    @property
    def discovered(self):
        return self._discovered

    @discovered.setter
    def discovered(self, value) -> None:
        self._discovered = value
        self.remove(self.value)
        self.value = Element(f"{value}/", color="#000000", font_size=DEFAULT_ELEMENT_FONT_SIZE - 2)
        self.value.move_to(self.container)
        self.add(self.value)

    @property
    def finished(self):
        raise RuntimeError()

    @finished.setter
    def finished(self, value) -> None:
        self.remove(self.value)
        self.value = Element(f"{self.discovered}/{value}", font_size=DEFAULT_ELEMENT_FONT_SIZE - 2)
        self.value.move_to(self.container)
        self.add(self.value)


class Edge(CustomVMobject):
    def __init__(self, start: Vertex, end: Vertex, directed: bool = True, dash_length: float | None = None) -> None:
        super().__init__()
        self.start = start
        self.end = end
        if dash_length is None:
            if self.start == self.end:
                self.line = ArcBetweenPoints(self.start.container.point_at_angle((5 * PI) / 4), self.end.container.point_at_angle((3 * PI) / 4), color="black", stroke_width=0.75, radius=-200)
            else:
                self.line = Line(self.start, self.end, color="black", stroke_width=0.75)
        else:
            self.line = DashedLine(self.start, self.end, color="black", stroke_width=0.75)

        self.line.add_tip(tip_length=0.1, tip_width=0.075)
        self.add(self.line)

        self.label: Element | None = None

    def add_label(self, label, on_edge: bool = False) -> None:
        self.label = Element(label, color="#000000")
        self.label.move_to(self)
        self.add(self.label)

    def is_back_edge(self) -> bool:
        # Self-loops are considered back edges
        if self.start == self.end:
            return True

        predecessor = self.start.predecessor
        while predecessor is not None:
            if predecessor == self.end:
                return True

            predecessor = predecessor.predecessor

        return False

    def is_forward_edge(self) -> bool:
        predecessor = self.end.predecessor
        while predecessor is not None:
            if predecessor == self.start:
                return True

            predecessor = predecessor.predecessor

        return False

    def is_cross_edge(self) -> bool:
        return True


class Graph(CustomVMobject):
    def __init__(self, adj_list: dict[Vertex, tuple[Vertex]], directed: bool = True):
        super().__init__()
        self.adj_list = adj_list
        self.edges: list[Edge] = []
        for vertex in adj_list.keys():
            self.add(vertex)

        for vertex, neighbors in adj_list.items():
            for n in neighbors:
                edge = Edge(vertex, n)
                self.edges.append(edge)
                self.add(edge)

    def _get_edge(self, start, end) -> Edge:
        for edge in self.edges:
            if edge.start == start and edge.end == end:
                return edge

        raise LookupError(f"Unable to find edge starting at {start} and ending at {end}")

    @property
    def vertices(self):
        return sorted([vertex for vertex in self.adj_list], key=lambda vertex : vertex.value.value)

    def depth_first_search(self, scene: Scene) -> None:
        # for vertex in self.vertices:
        #     vertex.color = NODE_WHITE
        #     vertex.predecessor = None
        scene.wait()
        visited = set()
        time: int = 0

        def _depth_first_search(vertex: Vertex) -> None:
            nonlocal time
            visited.add(vertex)
            time += 1
            vertex.discovered = time
            visited.add(vertex)
            vertex.container.set_style(fill_color=GRAY, fill_opacity=1)
            scene.wait()
            for neighbor in self.adj_list[vertex]:
                self._get_edge(vertex, neighbor).set(color=GRAY)
                if neighbor not in visited:
                    neighbor.predecessor = vertex
                    _depth_first_search(neighbor)
                else:
                    edge = self._get_edge(vertex, neighbor)
                    if edge.is_back_edge():
                        back_edge = Edge(edge.start, edge.end, dash_length=0.05)
                        back_edge.set(color=BLUE_D)
                        back_edge.add_label("B")
                        self.remove(edge)
                        self.add(back_edge)
                        scene.wait()
                    elif edge.is_forward_edge():
                        forward_edge = Edge(edge.start, edge.end, dash_length=0.05)
                        forward_edge.set(color=RED)
                        forward_edge.add_label("F")
                        self.remove(edge)
                        self.add(forward_edge)
                        scene.wait()
                    elif edge.is_cross_edge():
                        cross_edge = Edge(edge.start, edge.end, dash_length=0.05)
                        cross_edge.set(color=GOLD)
                        cross_edge.add_label("C")
                        self.remove(edge)
                        self.add(cross_edge)
                        scene.wait()
                    else:
                        raise RuntimeError(f"Unexpected edge type {edge}")

            # vertex.color = NODE_BLACK
            vertex.container.set_style(fill_color="#000000", fill_opacity=1)
            vertex.value.set(color="#FFFFFF")
            time += 1
            vertex.finished = time
            scene.wait()

        # breakpoint()
        for vertex in self.vertices:
            if vertex not in visited:
                _depth_first_search(vertex)


class MyScene(Scene):
    config["background_color"] = "#FFFFFF"
    config["disable_caching"] = True
    def construct(self):
        u = Vertex("u", 0, 0)
        v = Vertex("v", 1, 0)
        w = Vertex("w", 2, 0)
        x = Vertex("x", 0, -1)
        y = Vertex("y", 1, -1)
        z = Vertex("z", 2, -1)

        adj_list = {
            u: (v, x),
            v: (y,),
            x: (v,),
            y: (x,),
            w: (y, z),
            z: (z,),
        }

        graph = Graph(adj_list)
        graph.move_to([0, 0, 0])
        self.add(graph)
        self.wait()
        graph.adj_list[u][0].color = "#000000"
        self.wait()


        graph.depth_first_search(self)

    def wait(self, duration: float = 0.5):
        super().wait(0.5)


if __name__ == "__main__":
    MyScene().render()