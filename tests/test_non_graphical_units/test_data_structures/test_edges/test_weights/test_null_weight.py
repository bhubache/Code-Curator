from __future__ import annotations

from src.data_structures.edges.weights.null_weight import NullWeight


def test_value() -> None:
    assert NullWeight().value is None
