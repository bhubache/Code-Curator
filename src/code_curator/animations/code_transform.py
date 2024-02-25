from __future__ import annotations

from typing import TYPE_CHECKING

from manim import AnimationGroup
from manim import FadeOut
from manim import Succession
from manim import Transform

from code_curator.code import code_edit_parser

# from code_curator.animations.fixed_succession import FixedSuccession

if TYPE_CHECKING:
    from manim import Scene
    from code_curator.code.curator_code import CuratorCode


class CodeTransform(AnimationGroup):
    def __init__(
        self,
        original_code: CuratorCode,
        target_code: CuratorCode,
        methods,
        saturate_edits: bool,
        run_time: float = 1,
        **kwargs,
    ) -> None:
        self.mobjects_to_remove_on_cleanup = []
        self.methods = methods
        self.ungroupified_mobject = original_code
        matching_char_pairs, added_chars, removed_chars = code_edit_parser.partitioned_chars(original_code, target_code)

        for mob in added_chars:
            mob.set_opacity(0)
            original_code.add(mob)
            self.mobjects_to_remove_on_cleanup.append(mob)

        target_copies = []
        for _, target_mob in matching_char_pairs:
            target_mob_copy = target_mob.copy()
            target_mob_copy.set_opacity(0)
            original_code.add(target_mob_copy)
            target_copies.append(target_mob_copy)
            self.mobjects_to_remove_on_cleanup.append(target_mob_copy)

        if saturate_edits:
            decrease_opacity_and_fade_out_animation = AnimationGroup(
                *[mob.animate.set_opacity(0.15) for mob, _ in matching_char_pairs],
                *[FadeOut(mob) for mob in removed_chars],
            )

            transform_animation = AnimationGroup(
                *[Transform(original, target.set_opacity(0.15)) for original, target in matching_char_pairs],
            )

            fade_in_added_chars_animation = AnimationGroup(
                *[mob.animate.set_opacity(1) for mob in added_chars],
            )

            increase_opacity_back_to_normal_animation = AnimationGroup(
                *[mob.animate.set_opacity(1) for mob in target_copies],
            )

            super().__init__(
                Succession(
                    decrease_opacity_and_fade_out_animation,
                    transform_animation,
                    fade_in_added_chars_animation,
                    increase_opacity_back_to_normal_animation,
                ),
                run_time=run_time,
                **kwargs,
            )
        else:
            super().__init__(
                AnimationGroup(
                    *[Transform(original, target) for original, target in matching_char_pairs],
                    *[FadeOut(mob) for mob in removed_chars],
                ),
                AnimationGroup(
                    *[mob.animate.set_opacity(1) for mob in added_chars],
                ),
                lag_ratio=0.25,
                run_time=run_time,
                **kwargs,
            )

    def clean_up_from_scene(self, scene: Scene) -> None:
        super().clean_up_from_scene(scene)

        for mobject in self.mobjects_to_remove_on_cleanup:
            try:
                scene.remove(mobject)
            except ValueError:
                pass

            try:
                self.ungroupified_mobject.remove(mobject)
            except ValueError:
                pass

        # Apply all methods to self.mobject so it catches up to target in appearance
        for method, method_args, method_kwargs in self.methods:
            method.__func__(self.ungroupified_mobject, *method_args, **method_kwargs)
