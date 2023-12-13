from __future__ import annotations

import numpy as np
import pytest
from manim import DOWN
from manim import Point

from code_curator.data_structures.graph import Edge
from code_curator.data_structures.graph import Graph
from code_curator.data_structures.graph import LabeledLine
from code_curator.data_structures.graph import Vertex


@pytest.fixture
def graph() -> Graph:
    return Graph()


def test_empty_vertex() -> None:
    with pytest.raises(ValueError, match="You must provide at least the label or the contents of the"):
        Vertex()


def test_vertex_with_label() -> None:  # noqa: AAA01
    label = 0
    vertex = Vertex(label=label)

    assert vertex.label == label
    assert vertex.contents is None
    assert vertex.contents_mobject is None


def test_vertex_with_contents() -> None:
    contents = 0

    with pytest.raises(ValueError, match="You must provide a label for it to be shown"):
        Vertex(contents=contents)

    vertex = Vertex(contents=contents, show_label=False)
    assert vertex.contents == contents
    assert vertex.label is None
    assert vertex.label_mobject is None


EXCEPTION_MATCH = "You must provide Mobjects as the vertices"


def test_edge_passed_two_non_mobjects() -> None:
    with pytest.raises(TypeError, match=EXCEPTION_MATCH):
        Edge("a", "b")


def test_edge_passed_non_mobject_to_vertex_two() -> None:
    with pytest.raises(TypeError, match=EXCEPTION_MATCH):
        Edge(Vertex(0), "b")


def test_edge_passed_non_mobject_to_vertex_one() -> None:
    with pytest.raises(TypeError, match=EXCEPTION_MATCH):
        Edge("a", Vertex(1))


def test_edge() -> None:
    vertex_one = Vertex(0)
    vertex_two = Vertex(1)
    edge = Edge(vertex_one, vertex_two)

    assert edge.vertex_one == vertex_one
    assert edge.vertex_two == vertex_two


def test_graph(graph) -> None:
    assert len(graph.vertices) == 0
    assert len(graph.edges) == 0


def test_add_vertex_with_label(graph) -> None:
    graph.add_vertex(0)

    assert len(graph.vertices) == 1
    assert len(graph.edges) == 0


def test_add_vertex_with_vertex(graph) -> None:
    vertex = Vertex(0)

    graph.add_vertex(vertex)

    assert len(graph.vertices) == 1
    assert vertex in graph.vertices
    assert len(graph.edges) == 0


def test_add_edge_with_non_mobject_vertices(graph) -> None:
    vertex_one = Vertex(0)
    vertex_two = Vertex(1)

    graph.add_vertex(vertex_one)
    graph.add_vertex(vertex_two)
    graph.add_edge(0, 1)

    assert len(graph.vertices) == 2
    assert vertex_one in graph.vertices
    assert vertex_two in graph.vertices
    assert len(graph.edges) == 1


def test_add_edge_with_mobject_vertices(graph) -> None:
    vertex_one = Vertex(0)
    vertex_two = Vertex(1)

    graph.add_vertex(vertex_one)
    graph.add_vertex(vertex_two)
    graph.add_edge(vertex_one, vertex_two)

    assert len(graph.vertices) == 2
    assert vertex_one in graph.vertices
    assert vertex_two in graph.vertices
    assert len(graph.edges) == 1


def test_remove_single_vertex(graph) -> None:
    vertex_one = Vertex(0)

    graph.add_vertex(vertex_one)
    graph.remove(vertex_one)

    assert len(graph.vertices) == 0
    assert len(graph.edges) == 0
    assert len(graph.submobjects) == 0


def test_remove_single_vertex_from_multi_vertex_graph(graph) -> None:
    vertex_one = Vertex(0)
    vertex_two = Vertex(1)

    graph.add_vertex(vertex_one)
    graph.add_vertex(vertex_two)
    graph.remove(vertex_one)

    assert len(graph.vertices) == 1
    assert vertex_two in graph.vertices
    assert len(graph.edges) == 0
    assert len(graph.submobjects) == 1
    assert vertex_two in graph.submobjects


def test_remove_edge(graph) -> None:
    vertex_one = Vertex(0)
    vertex_two = Vertex(1)

    graph.add_vertex(vertex_one)
    graph.add_vertex(vertex_two)
    graph.add_edge(vertex_one, vertex_two)

    for e in graph.edges:
        edge = e

    graph.remove(edge)

    assert len(graph.vertices) == 2
    assert vertex_one in graph.vertices
    assert vertex_two in graph.vertices
    assert len(graph.edges) == 0
    assert len(graph.submobjects) == 2
    assert vertex_one in graph.submobjects
    assert vertex_two in graph.submobjects


def test_remove_start_vertex_connected_by_edge(graph) -> None:
    vertex_one = Vertex(0)
    vertex_two = Vertex(1)

    graph.add_vertex(vertex_one)
    graph.add_vertex(vertex_two)
    graph.add_edge(vertex_one, vertex_two)
    graph.remove(vertex_one)

    assert len(graph.vertices) == 1
    assert vertex_two in graph.vertices
    assert len(graph.edges) == 1
    edge = next(iter(graph.edges))
    assert edge.vertex_one is None
    assert edge.vertex_two is vertex_two
    assert len(graph.submobjects) == 2
    assert vertex_two in graph.submobjects
    assert edge in graph.submobjects


def test_remove_end_vertex_connected_by_edge(graph) -> None:
    vertex_one = Vertex(0)
    vertex_two = Vertex(1)

    graph.add_vertex(vertex_one)
    graph.add_vertex(vertex_two)
    graph.add_edge(vertex_one, vertex_two)
    graph.remove(vertex_two)

    assert len(graph.vertices) == 1
    assert vertex_one in graph.vertices
    assert len(graph.edges) == 1
    edge = next(iter(graph.edges))
    assert edge.vertex_two is None
    assert edge.vertex_one is vertex_one
    assert len(graph.submobjects) == 2
    assert vertex_one in graph.submobjects
    assert edge in graph.submobjects


def test_get_vertex(graph) -> None:
    graph.add_vertex(0)
    graph.add_vertex(1)

    vertex = Vertex(2)
    graph.add_vertex(vertex)

    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)

    assert graph.get_vertex(2) is vertex


def test_labeled_line_by_coordinates() -> None:
    labeled_line = LabeledLine([0, 0, 0], [1, 0, 0])

    assert np.array_equal(labeled_line.start, [0, 0, 0])
    assert np.array_equal(labeled_line.end, [1, 0, 0])
    assert labeled_line.label == ""
    with pytest.raises(AttributeError):
        labeled_line.pointee


def test_labeled_line_pointing_to_mobject() -> None:
    vertex = Vertex(0)
    length = 1
    direction = DOWN
    labeled_line = LabeledLine(vertex, length=length, direction=direction)

    end = vertex.get_boundary_point(-direction)
    start = Point(end).shift(-direction * length).get_boundary_point(direction)

    for observed_component, expected_component in zip(labeled_line.start, start):
        assert np.isclose(observed_component, expected_component)

    for observed_component, expected_component in zip(labeled_line.end, end):
        assert np.isclose(observed_component, expected_component)


def test_labeled_line_by_single_coordinate() -> None:
    coordinate = (0, 0, 0)
    length = 1
    direction = DOWN
    labeled_line = LabeledLine(coordinate, length=length, direction=direction)

    assert np.array_equal(labeled_line.start, [0, 1, 0])
    assert np.array_equal(labeled_line.end, coordinate)
