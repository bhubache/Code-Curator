from __future__ import annotations

import math


def degrees_to_radians(angle_in_degrees: float) -> float:
    """Convert ``angle_in_degrees`` to radians."""
    return (angle_in_degrees * math.pi) / 180


def value_from_range_to_range(
    value: float,
    init_min: float,
    init_max: float,
    new_min: float,
    new_max: float,
) -> float:
    # TODO: Comment an explanation for this
    return new_min + ((new_max - new_min) / (init_max - init_min)) * (value - init_min)
