from __future__ import annotations

from typing import TYPE_CHECKING

from manim import AnimationGroup
from manim import FadeIn
from manim import FadeOut
from manim import Transform

from code_curator.animations.fixed_succession import FixedSuccession
from code_curator.code import code_edit_parser

if TYPE_CHECKING:
    from manim import Paragraph
    from manim import VGroup
    from manim import Scene
    from code_curator.code.curator_code import CuratorCode


class CodeTransform(AnimationGroup):
    def __init__(
        self,
        original_code: CuratorCode,
        target_code: CuratorCode,
        methods,
        saturate_edits: bool,
        **kwargs,
    ) -> None:
        matching_line_pairs: list[tuple[VGroup, VGroup]] = []
        added_lines: list[VGroup] = []
        removed_lines: list[VGroup] = []
        changed_code_pairs: list[tuple[VGroup, VGroup, bool]] = []

        bounds_to_leave_saturated: list[tuple[int, int, int]] = []

        source_line_index = 0
        target_line_index = 0
        source_code_lines: Paragraph = original_code.code_paragraph
        target_code_lines: Paragraph = target_code.code_paragraph

        for unprocessed_line in target_code.unprocessed_str_lines:
            try:
                source_line: VGroup | None = source_code_lines[source_line_index]
            except IndexError:  # Only lines unique to the target code remain
                source_line: VGroup | None = None

            try:
                target_line: VGroup | None = target_code_lines[target_line_index]
            except IndexError:  # Only lines unique to the source code remain
                target_line: VGroup | None = None

            if not code_edit_parser.line_changed(unprocessed_line):
                matching_line_pairs.append(
                    (
                        source_line,
                        target_line,
                    ),
                )
                source_line_index += 1
                target_line_index += 1
            elif code_edit_parser.line_is_added(unprocessed_line):
                added_lines.append(target_line)
                target_line_index += 1
            elif code_edit_parser.line_is_removed(unprocessed_line):
                removed_lines.append(source_line)
                source_line_index += 1
            elif code_edit_parser.line_is_edited(unprocessed_line):
                for (
                    source_start,
                    source_end,
                    target_start,
                    target_end,
                    is_edited,
                ) in code_edit_parser.pairwise_edited_line_bounds(
                    unprocessed_line,
                ):
                    changed_code_pairs.append(
                        (
                            source_line[source_start:source_end],
                            target_line[target_start:target_end],
                            is_edited,
                        ),
                    )

                    if is_edited:
                        bounds_to_leave_saturated.append(
                            (source_line_index, source_start, source_end),
                        )

                source_line_index += 1
                target_line_index += 1
            else:
                raise RuntimeError(f"Unexpected code line to transform: {unprocessed_line}")

        self.mobjects_to_remove_on_cleanup: list[VGroup] = []
        for line in added_lines:
            self.mobjects_to_remove_on_cleanup.append(line)

        for source_mobject, *_ in changed_code_pairs:
            original_code.add(source_mobject)
            self.mobjects_to_remove_on_cleanup.append(source_mobject)

        if saturate_edits:
            fade_out_and_desaturate_animations = [
                original_code.code_paragraph.animate.set_opacity(0.15),
            ]

            for source_line_index, start, end in bounds_to_leave_saturated:
                fade_out_and_desaturate_animations.append(
                    FadeOut(original_code.code_paragraph[source_line_index][start:end]),
                )

            fade_in_and_transform_animations = []
            editing_started = False
            for source_line, target_line, is_edited in changed_code_pairs:
                if is_edited:
                    editing_started = True

                    target_line.set_opacity(0)
                    original_code.add(target_line)
                    self.mobjects_to_remove_on_cleanup.append(target_line)

                    fade_in_and_transform_animations.append(target_line.animate.set_opacity(1))
                    continue

                if editing_started:
                    fade_in_and_transform_animations.append(Transform(source_line, target_line.set_opacity(0.15)))

            super().__init__(
                FixedSuccession(
                    AnimationGroup(
                        *fade_out_and_desaturate_animations,
                    ),
                    AnimationGroup(
                        *fade_in_and_transform_animations,
                    ),
                    target_code.animate.set_opacity(1),
                ),
                **kwargs,
            )
        else:
            super().__init__(
                AnimationGroup(
                    *[Transform(source_line, target_line) for source_line, target_line in matching_line_pairs],
                    *[FadeOut(line) for line in removed_lines],
                    *[Transform(source_code, target_code) for source_code, target_code, _ in changed_code_pairs],
                ),
                AnimationGroup(
                    *[FadeIn(line) for line in added_lines],
                ),
                lag_ratio=0.25,
                **kwargs,
            )

        self.ungroupified_mobject = original_code
        self.methods = methods

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
