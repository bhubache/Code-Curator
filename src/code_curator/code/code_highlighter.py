from __future__ import annotations

from typing import TYPE_CHECKING

from manim import Code
from manim import DOWN
from manim import LEFT
from manim import Rectangle
from manim import YELLOW

if TYPE_CHECKING:
    from code_curator.code.curator_code import CuratorCode
    from colour import Color


class CodeHighlighter(Rectangle):
    def __init__(
        self,
        code: CuratorCode,
        height: float | None = None,
        width: float | None = None,
        color: str | Color = YELLOW,
        stroke_width: float = 0.0,
        start_line: int = 1,
    ) -> None:
        if height is None:
            height = code.max_line_height

        if width is None:
            width = code.max_line_width

        super().__init__(height=height, width=width, color=color, stroke_width=stroke_width)

        self.code = code
        self.curr_line_num = start_line
        self.set_opacity(0.5)
        self.align_to(self.code.get_line(self.curr_line_num), DOWN)
        self.align_to(self.code.get_line(self.curr_line_num), LEFT)

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

    def move_to_line(self, line_num: int) -> None:
        if line_num < 1 or line_num > self.code.num_lines:
            raise ValueError(
                f"``line_num`` must be in range [1, {self.code.num_lines}]. Given {line_num}"
            )

        self.curr_line_num = line_num

        return self.animate.become(CodeHighlighter(self.code).align_to(self.code.get_line(self.curr_line_num), DOWN))
