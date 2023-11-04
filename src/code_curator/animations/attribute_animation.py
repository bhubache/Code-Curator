from __future__ import annotations

from manim import Animation
from manim import Mobject

from .utils import math_


class AttributeAnimation(Animation):
    def __init__(self, mobject: Mobject, *, attribute: str, value, **kwargs):
        super().__init__(mobject, **kwargs)
        self.attribute = attribute
        self.target_value = value
        self.initial_value = getattr(mobject, attribute)

    def interpolate_mobject(self, alpha: float):
        setter = getattr(
            self.mobject,
            f"set_{self.attribute}",
        )

        setter(
            math_.value_from_range_to_range(
                value=alpha,
                init_min=0,
                init_max=self.target_value,
                new_min=0,
                new_max=1.0,
            ),
        )
