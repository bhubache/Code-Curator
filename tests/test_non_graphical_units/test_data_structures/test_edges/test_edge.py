from __future__ import annotations

import numpy as np
import pytest
from colour import Color
from constants import DEFAULT_MOBJECT_COLOR
from constants import DEFAULT_STROKE_WIDTH
from data_structures.edges.edge import Edge
from data_structures.edges.weights.null_weight import NullWeight
from manim import Line


@pytest.fixture
def default_edge() -> Edge:
    return Edge()


def test_default_start(default_edge: Edge) -> None:
    assert np.array_equal(default_edge.start, np.array([-1, 0, 0]))


def test_default_end(default_edge: Edge) -> None:
    assert np.array_equal(default_edge.end, np.array([1, 0, 0]))


def test_default_weight(default_edge: Edge) -> None:
    assert default_edge.weight == NullWeight()


def test_default_color(default_edge: Edge) -> None:
    assert default_edge.color == DEFAULT_MOBJECT_COLOR


def test_default_stroke_width(default_edge: Edge) -> None:
    assert default_edge.stroke_width == DEFAULT_STROKE_WIDTH


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
    return Edge(
        start=[-1, -2, 0], end=[2, 2, 0], color='#cfeb34', line_stroke_width=5, weight=16.0,
    )


def test_custom_start(custom_edge: Edge) -> None:
    assert np.array_equal(custom_edge.start, np.array([-1, -2, 0]))


def test_custom_end(custom_edge: Edge) -> None:
    assert np.array_equal(custom_edge.end, np.array([2, 2, 0]))


def test_custom_weight(custom_edge: Edge) -> None:
    assert custom_edge.weight.equals(16.0)


def test_custom_color(custom_edge: Edge) -> None:
    assert custom_edge.color == Color('#cfeb34')


def test_custom_stroke_width(custom_edge: Edge) -> None:
    assert custom_edge.stroke_width == 5


def test_custom_vertical_length(custom_edge: Edge) -> None:
    assert custom_edge.vertical_length == 4


def test_custom_horizontal_length(custom_edge: Edge) -> None:
    assert custom_edge.horizontal_length == 3


def test_custom_length(custom_edge: Edge) -> None:
    assert custom_edge.length == 5
