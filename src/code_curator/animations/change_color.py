from __future__ import annotations

from typing import TYPE_CHECKING

from manim import Animation
from manim import interpolate_color
from manim import smooth


if TYPE_CHECKING:
    from colour import Color
    from manim import Mobject


class ChangeColor(Animation):
    def __init__(
        self,
        mobject: Mobject,
        color: str | Color,
        starting_color: str | Color | None = None,
        **kwargs,
    ) -> None:
        super().__init__(mobject, run_time=kwargs.pop("run_time", None), **kwargs)
        self.initial_color = mobject.color
        self.target_color = color

        if starting_color is not None:
            self.initial_color = starting_color

    def interpolate(self, alpha: float) -> None:
        curr_color = interpolate_color(
            self.initial_color, self.target_color, smooth(alpha)
        )
        self.mobject.set_color(curr_color)
