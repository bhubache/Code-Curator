from __future__ import annotations

import math


def degrees_to_radians(angle_in_degrees: float) -> float:
    """Convert ``angle_in_degrees`` to radians."""
    return (angle_in_degrees * math.pi) / 180
