import numpy as np
import pytest

from src.data_structures.edges.edge import Edge
from src.constants import DEFAULT_MOBJECT_COLOR

@pytest.fixture
def default_edge() -> Edge:
    return Edge()

def test_default_edge_start(default_edge: Edge) -> None:
    assert np.array_equal(default_edge.start, np.array([-1, 0, 0]))

def test_default_edge_end(default_edge: Edge) -> None:
    assert np.array_equal(default_edge.end, np.array([1, 0, 0]))

def test_default_edge_color(default_edge: Edge) -> None:
    assert default_edge.color == DEFAULT_MOBJECT_COLOR
