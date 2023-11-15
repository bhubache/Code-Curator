from __future__ import annotations

import math

from manim import BLACK
from manim import Circle
from manim import Mobject

from code_curator.constants import DEFAULT_ELEMENT_FONT_SIZE
from code_curator.custom_vmobject import CustomVMobject
from code_curator.data_structures.element import Element


class Graph(CustomVMobject):
    def add_vertex(
        self,
        label,
        *,
        contents: Mobject | None = None,
        container: Mobject | None = None,
        position: tuple[float, float, float] = (0.0, 0.0, 0.0),
        label_out: bool = False,
        label_dist: float = 0.0,
        label_revolve_angle_in_degrees: float = 0.0,
        label_rotate_angle_in_degrees: float = 0.0,
        show_label: bool = True,
    ) -> None:
        if container is None:
            container = Circle(color=BLACK, radius=0.2, stroke_width=0.75)

        label = Element(label, color=BLACK, font_size=DEFAULT_ELEMENT_FONT_SIZE - 2)
        if label_out:
            circumscribing_circle = Circle(stroke_width=0.75).surround(
                container,
                buffer_factor=1 + label_dist,
            )
            label.move_to(
                circumscribing_circle.point_at_angle(
                    math.radians(label_revolve_angle_in_degrees),
                ),
            )

        container.add(label)

        if contents is not None:
            contents = Element(
                contents,
                color=BLACK,
                font_size=DEFAULT_ELEMENT_FONT_SIZE - 2,
            )
            container.add(contents)

        container.move_to(position)

        self.add(container)
