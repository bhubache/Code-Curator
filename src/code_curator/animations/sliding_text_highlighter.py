from __future__ import annotations

import itertools as it
from typing import TYPE_CHECKING

from manim import Animation
from manim import LEFT
from manim import ParsableManimColor
from manim import Rectangle
from manim import Tex
from manim import Text
from manim import YELLOW

from code_curator.animations.utils.math_ import value_from_range_to_range

if TYPE_CHECKING:
    from manim import VGroup


class SlidingTextHighlighter(Animation):
    def __init__(
        self,
        text: Text | Tex,
        color: ParsableManimColor = YELLOW,
        opacity: float = 0.5,
        run_time: float = 1.0,
    ) -> None:
        super().__init__(text, run_time=run_time, introducer=True)
        self.text = text
        self.color = color
        self.opacity = opacity
        self.rectangle_height = max(word.height for word in self.text)

        self.text_partitions = self._get_text_partitions()
        self.start_rectangles = self._get_start_rectangles()
        self.start_end_alphas = self._get_start_end_alphas()

        for start_rectangle in self.start_rectangles:
            self.mobject.add(start_rectangle)

    def interpolate(self, alpha: float) -> None:
        for text_line, start_rectangle, (start_alpha, end_alpha) in zip(
            self.text_partitions,
            self.start_rectangles,
            self.start_end_alphas,
        ):
            sub_alpha = value_from_range_to_range(
                init_min=start_alpha,
                init_max=end_alpha,
                new_min=0,
                new_max=1,
                value=alpha,
                clip=True,
            )

            start_rectangle.become(
                Rectangle(
                    height=self.rectangle_height,
                    width=text_line.width * sub_alpha,
                )
                .move_to(text_line.get_center())
                .align_to(text_line, LEFT)
                .match_style(start_rectangle),
            )

    def _get_text_partitions(self) -> list[VGroup]:
        """Return text chunks partitioned by the rectangle that will highlight them."""
        rectangle_start_indices = [0]
        furthest_left_seen = self.text[0].get_left()[0]
        for index, word in enumerate(self.text[1:], start=1):
            curr_word_left = word.get_left()[0]
            if curr_word_left < furthest_left_seen:
                rectangle_start_indices.append(index)
                furthest_left_seen = curr_word_left

        text_lines = []
        for start, end in it.pairwise(rectangle_start_indices + [len(self.text)]):
            text_lines.append(self.text[start:end])

        return text_lines

    def _get_start_rectangles(self):
        return [
            Rectangle(
                color=self.color,
                height=self.rectangle_height,
                width=0,
                fill_color=self.color,
                fill_opacity=self.opacity,
                stroke_width=0,
            )
            .move_to(text_line.get_center())
            .align_to(text_line, LEFT)
            for text_line in self.text_partitions
        ]

    def _get_start_end_alphas(self):
        starting_alphas = []
        width_of_seen_rectangles = 0
        total_width = sum(line.width for line in self.text_partitions)
        for line in self.text_partitions:
            starting_alphas.append(
                width_of_seen_rectangles / total_width,
            )
            width_of_seen_rectangles += line.width

        start_end_alphas = []
        for prev_alpha, next_alpha in it.pairwise(starting_alphas + [1]):
            start_end_alphas.append(
                (
                    prev_alpha,
                    next_alpha,
                ),
            )

        return start_end_alphas
