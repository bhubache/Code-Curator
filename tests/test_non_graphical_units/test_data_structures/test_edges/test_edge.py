import numpy as np
import pytest

from src.data_structures.edges.edge import Edge
from manim import Line
from src.constants import DEFAULT_MOBJECT_COLOR, DEFAULT_STROKE_WIDTH

@pytest.fixture
def default_edge() -> Edge:
    return Edge()

def test_default_start(default_edge: Edge) -> None:
    assert np.array_equal(default_edge.start, np.array([-1, 0, 0]))

def test_default_end(default_edge: Edge) -> None:
    assert np.array_equal(default_edge.end, np.array([1, 0, 0]))

def test_default_weight(default_edge: Edge) -> None:
    assert default_edge.weight is None

def test_default_vertical_length(default_edge: Edge) -> None:
    assert default_edge.vertical_length == 0

def test_default_horizontal_length(default_edge: Edge) -> None:
    assert default_edge.horizontal_length == 2

def test_default_length(default_edge: Edge) -> None:
    assert default_edge.length == 2

def test_default_line(default_edge: Edge) -> None:
    assert type(default_edge.line) == Line


@pytest.fixture
def custom_edge() -> Edge:
    return Edge(start=[-1, -2, 0], end=[2, 2, 0], line_color='#FFFFFF', line_stroke_width=5, weight=16)

def test_custom_start(custom_edge: Edge) -> None:
    assert np.array_equal(custom_edge.start, np.array([-1, -2, 0]))

def test_custom_end(custom_edge: Edge) -> None:
    assert np.array_equal(custom_edge.end, np.array([2, 2, 0]))

def test_custom_weight(custom_edge: Edge) -> None:
    assert custom_edge.weight == 16

def test_custom_vertical_length(custom_edge: Edge) -> None:
    assert custom_edge.vertical_length == 4

def test_custom_horizontal_length(custom_edge: Edge) -> None:
    assert custom_edge.horizontal_length == 3

def test_custom_length(custom_edge: Edge) -> None:
    assert custom_edge.length == 5
