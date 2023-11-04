from __future__ import annotations

from manim import Animation
from manim import Arrow
from manim import Mobject
from manim import ShrinkToCenter
from manim import GrowArrow
from manim import GrowFromCenter
from manim import Scene

from code_curator.animations.utils.math_ import value_from_range_to_range


class ArrowTransportTransformation(Animation):
    def __init__(
        self,
        mobject: Mobject,
        target_mobject: Mobject,
    ) -> None:
        container_mobject = Mobject()
        super().__init__(container_mobject)
        self.base_mobject = mobject
        self.target_mobject = target_mobject
        self.arrow = Arrow(
            start=self.base_mobject.get_center(),
            end=self.target_mobject.get_center(),
            color=self.base_mobject.color,
            tip_length=0.25,
            stroke_width=1.5,
        )

        self.shrink_base_mob_animation = ShrinkToCenter(self.base_mobject)
        self.grow_arrow_animation = GrowArrow(self.arrow)
        self.grow_target_mob_animation = GrowFromCenter(self.target_mobject)

        self.halfway_point_reached = False

    def begin(self):
        self.mobject.add(self.base_mobject)
        self.mobject.add(self.arrow)
        self.mobject.add(self.target_mobject)

        self.shrink_base_mob_animation.begin()
        self.grow_arrow_animation.begin()
        self.grow_target_mob_animation.begin()
        super().begin()

    def interpolate_mobject(self, alpha: float) -> None:
        if alpha < 0.5:
            converted_alpha = value_from_range_to_range(
                value=alpha,
                init_min=0,
                init_max=0.5,
                new_min=0,
                new_max=1,
            )

            self.shrink_base_mob_animation.interpolate_mobject(converted_alpha)
            self.grow_arrow_animation.interpolate_mobject(converted_alpha)

        else:
            converted_alpha = value_from_range_to_range(
                value=alpha,
                init_min=0.5,
                init_max=1,
                new_min=0,
                new_max=1,
            )

            self.grow_target_mob_animation.interpolate_mobject(converted_alpha)
            self.arrow.scale(1 - converted_alpha, scale_tips=True)
            self.arrow.move_to(self.target_mobject.get_center(), aligned_edge=self.arrow.get_end())

    def clean_up_from_scene(self, scene: Scene) -> None:
        super().clean_up_from_scene(scene)
        self.shrink_base_mob_animation.clean_up_from_scene(scene)
        self.grow_arrow_animation.clean_up_from_scene(scene)
        self.grow_target_mob_animation.clean_up_from_scene(scene)


