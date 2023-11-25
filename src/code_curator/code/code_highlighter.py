from __future__ import annotations

from typing import TYPE_CHECKING

from manim import Code
from manim import DOWN
from manim import LEFT
from manim import Rectangle
from manim import YELLOW

if TYPE_CHECKING:
    from colour import Color


class CodeHighlighter(Rectangle):
    def __init__(
        self,
        code: Code,
        height: float | None = None,
        width: float | None = None,
        color: str | Color = YELLOW,
        stroke_width: float = 0.0,
    ) -> None:
        if height is None:
            height = code.max_line_height

        if width is None:
            width = code.max_line_width

        super().__init__(height=height, width=width, color=color, stroke_width=stroke_width)

        self.code = code
        self.curr_line_num = 0
        self.set_opacity(0.5)
        self.align_to(self.code.code[self.curr_line_num], DOWN)
        self.align_to(self.code.code[self.curr_line_num], LEFT)

    def move_to_substring(self, substring: str, occurrence: int, num_lines: int | None):
        """
        For the line the highlighter is on, you can specify a substring for the
        highlighter to cover
        """
        if num_lines is not None:
            raise NotImplementedError()

        code_substring = self.code.get_code_substring(
            substring,
            occurrence=occurrence,
        )

        new_highlighter = (
            CodeHighlighter(
                code=self.code,
                width=code_substring.width,
            )
            .align_to(code_substring, DOWN)
            .align_to(code_substring, LEFT)
        )

        return self.animate.become(new_highlighter)

    def move(self, num_lines: int) -> None:
        new_line_num = self.curr_line_num + num_lines
        if new_line_num < 0 or new_line_num >= self.code.num_lines:
            raise IndexError(
                f"{new_line_num} is out of bounds for {self.code.num_lines}",
            )

        self.curr_line_num = new_line_num

        return self.animate.become(CodeHighlighter(self.code).align_to(self.code.code[new_line_num], DOWN))
