from __future__ import annotations

from manim import AnimationGroup
from manim import Code
from manim import FadeIn
from manim import FadeOut

from code_curator.code.code_diff import CodeDiff


class CodeTransform(AnimationGroup):
    def __init__(
        self,
        original_code: Code,
        target_code: Code,
    ):
        self.mobject = original_code
        self.target_mobject = target_code
        self.code_diff = CodeDiff(self.mobject, self.target_mobject)

        for line in self.code_diff.added_lines:
            self.mobject.add(line)

        changed_line_animations = []
        for record in self.code_diff.changed_line_pairs:
            for animation in record.animations:
                try:
                    is_introducer = animation.is_introducer()
                except AttributeError:
                    continue
                else:
                    if is_introducer:
                        self.mobject.add(animation.mobject)

            changed_line_animations.extend(record.animations)

        super().__init__(
            AnimationGroup(
                AnimationGroup(
                    *(
                        [FadeOut(line) for line in self.code_diff.removed_lines]
                        + [
                            source_line.animate.move_to(destination_line)
                            for source_line, destination_line in self.code_diff.matching_line_pairs
                        ]
                        + changed_line_animations
                    ),
                ),
                AnimationGroup(
                    *[FadeIn(line) for line in self.code_diff.added_lines],
                ),
                lag_ratio=0.25,
            ),
        )
