from __future__ import annotations

from typing import TYPE_CHECKING

from manim import LEFT
from manim import Rectangle
from manim import YELLOW
from manim.mobject.text.text_mobject import remove_invisible_chars

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
        opacity: float = 0.2,
        stroke_width: float = 0.0,
        start_line: int = 1,
        height_buff: float = 0.05,
        width_buff: float = 0.1,
    ) -> None:
        if height is None:
            height = code.max_line_height + height_buff

        if width is None:
            width = code.max_line_width + width_buff

        self.height_buff = height_buff
        self.width_buff = width_buff
        super().__init__(height=height, width=width, color=color, stroke_width=stroke_width)

        self.code = code
        self.curr_line_num = start_line
        self.set_opacity(opacity)
        self.move_to_line(start_line)

    def reset_height(self):
        return self.stretch_to_fit_height(self.code.max_line_height + self.height_buff)

    def reset_width(self):
        return self.stretch_to_fit_width(self.code.max_line_width + self.width_buff)

    def move_to_substring(self, substring: str, occurrence: int, num_lines: int | None):
        """
        For the line the highlighter is on, you can specify a substring for the
        highlighter to cover
        """
        if num_lines is not None:
            raise NotImplementedError()

        code_substring_line = self.code.get_code_substring_line(
            substring,
            occurrence=occurrence,
        )

        code_substring = self.code.get_code_substring(
            substring,
            occurrence=occurrence,
        )

        try:
            to_line_copy_with_only_visible_chars = remove_invisible_chars(code_substring_line.copy())
        except IndexError:
            to_line_copy_with_only_visible_chars = code_substring_line.copy()

        self.stretch_to_fit_width(code_substring.width + self.width_buff)
        self.move_to(to_line_copy_with_only_visible_chars.get_center())
        self.align_to(code_substring, LEFT)
        self.shift(LEFT * (self.width_buff / 2))

        return self

    def move_to_line(self, line_num: int):
        if line_num < 1 or line_num > self.code.num_lines:
            raise ValueError(
                f"``line_num`` must be in range [1, {self.code.num_lines}]. Given {line_num}",
            )

        self.reset_height()
        self.reset_width()

        to_line_copy = self.code.get_line(line_num).copy()
        try:
            to_line_copy_with_only_visible_chars = remove_invisible_chars(to_line_copy)
        except IndexError:
            to_line_copy_with_only_visible_chars = self.code.get_line(line_num).copy()

        self.move_to(to_line_copy_with_only_visible_chars.get_center())
        self.align_to(self.code.code_mobject, LEFT)
        self.shift(LEFT * (self.width_buff / 2))

        self.curr_line_num = line_num

        return self
