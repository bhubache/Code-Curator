from __future__ import annotations

import pytest


def test_not_using_manim_property_raises_error() -> None:
    with pytest.raises(Exception):
        assert False
