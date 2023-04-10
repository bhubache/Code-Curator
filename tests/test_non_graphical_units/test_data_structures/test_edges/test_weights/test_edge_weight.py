from __future__ import annotations

import pytest
from colour import Color

from src.constants import DEFAULT_ELEMENT_FONT_SIZE
from src.constants import DEFAULT_MOBJECT_COLOR
from src.data_structures.edges.weights.edge_weight import EdgeWeight
from src.data_structures.edges.weights.weight import Weight

FIVE_INT: int = 5
FIVE_FLOAT: float = 5.0


@pytest.fixture
def weight_five_int() -> Weight:
    return EdgeWeight(FIVE_INT)


@pytest.fixture
def weight_five_float() -> Weight:
    return EdgeWeight(FIVE_FLOAT)


def test_value_int_positional_arg() -> None:
    weight: EdgeWeight = EdgeWeight(FIVE_INT)
    assert weight.value == FIVE_INT


def test_value_int_keyword_arg() -> None:
    weight: EdgeWeight = EdgeWeight(value=FIVE_INT)
    assert weight.value == FIVE_INT


def test_value_int(weight_five_int: EdgeWeight) -> None:
    assert weight_five_int.value == FIVE_INT


def test_value_float(weight_five_float: EdgeWeight) -> None:
    assert weight_five_float.value == FIVE_FLOAT


def test_default_color() -> None:
    weight: EdgeWeight = EdgeWeight(0)
    assert weight.get_color() == DEFAULT_MOBJECT_COLOR


def test_default_font_size() -> None:
    weight: EdgeWeight = EdgeWeight(0)
    assert weight.font_size == DEFAULT_ELEMENT_FONT_SIZE


def test_dunder_str() -> None:
    weight: EdgeWeight = EdgeWeight(100)
    assert str(weight) == '100'


def test_equals_method_with_int() -> None:
    assert EdgeWeight(5).equals(5)


def test_equals_method_with_int_not() -> None:
    assert not EdgeWeight(5).equals(6)


def test_equals_method_with_float() -> None:
    assert EdgeWeight(5.0).equals(5.0)


def test_equals_method_with_float_not() -> None:
    assert not EdgeWeight(5.0).equals(6.0)


def test_equals_method_with_edge_weight_int() -> None:
    assert EdgeWeight(5).equals(EdgeWeight(5))


def test_equals_method_with_edge_weight_int_not() -> None:
    assert not EdgeWeight(5).equals(EdgeWeight(6))


def test_equals_method_with_edge_weight_float() -> None:
    assert EdgeWeight(5.0).equals(EdgeWeight(5.0))


def test_equals_method_with_edge_weight_float_not() -> None:
    assert not EdgeWeight(5.0).equals(EdgeWeight(6.0))


def test_equals_method_invalid_type() -> None:
    with pytest.raises(NotImplementedError):
        assert EdgeWeight(5).equals('some string')  # type: ignore


def test_equality() -> None:
    assert EdgeWeight(16) != EdgeWeight(16)


def test_set_color_str() -> None:
    edge_weight: EdgeWeight = EdgeWeight(5)
    edge_weight.set_color('#FFFFFF')
    assert edge_weight.get_color() == Color('#FFFFFF')


def test_set_color_color() -> None:
    edge_weight: EdgeWeight = EdgeWeight(5)
    edge_weight.set_color(Color('#FFFFFF'))
    assert edge_weight.get_color() == Color('#FFFFFF')
