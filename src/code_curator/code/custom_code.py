from __future__ import annotations

import itertools as it
import math

from manim import Animation
from manim import Code

from code_curator.animations.code_transform import CodeTransform
from code_curator.animations.singly_linked_list.transform_sll import TransformSinglyLinkedList
from code_curator.code.code_highlighter import CodeHighlighter


class CustomCode(Code):
    def __init__(
        self,
        file_name: str | None = None,
        tab_width: int = 1,
        indentation_chars: str = " ",
        font="Monospace",
        font_size=24,
        stroke_width=0,
        margin: float = 0.1,
        background: str | None = None,
        background_stroke_width: float = 0,
        background_stroke_color: str = "#FFFFFF",
        corner_radius=0.0,
        insert_line_no: bool = False,
        line_spacing: float = 0.5,
        line_no_buff: float = 0.2,
        style: str = "nord",
        language: str = "python",
        background_color: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            file_name=file_name,
            tab_width=tab_width,
            indentation_chars=indentation_chars,
            font=font,
            font_size=font_size,
            stroke_width=stroke_width,
            margin=margin,
            background=background,
            background_stroke_width=background_stroke_width,
            background_stroke_color=background_stroke_color,
            corner_radius=corner_radius,
            insert_line_no=insert_line_no,
            line_spacing=line_spacing,
            line_no_buff=line_no_buff,
            style=style,
            language=language,
            **kwargs,
        )
        self.background_mobject.set_opacity(0)
        self._highlighter = None

        self.scale(0.5)

    @property
    def num_lines(self) -> int:
        return len(self.code)

    @property
    def max_line_height(self):
        # It looks like lines that immediately following an empty line have the height for both of them.
        #  So, exclude those lines.
        lines_to_consider = [self.code[0].height]
        for prev_line, curr_line in it.pairwise(self.code):
            if math.isclose(prev_line.height, 0):
                continue

            lines_to_consider.append(curr_line.height)

        return max(lines_to_consider)

    @property
    def max_line_width(self):
        # I want the max line width including the indentation chars at the beginning of a line
        min_starting_x = min(line.get_left()[0] for line in self.code)
        max_ending_x = max(line.get_right()[0] for line in self.code)
        return max_ending_x - min_starting_x

    @property
    def highlighter(self) -> CodeHighlighter:
        return self._highlighter

    @highlighter.setter
    def highlighter(self, highlighter: CodeHighlighter) -> None:
        self._highlighter = highlighter
        self._highlighter.code = self

    # TODO: Give better name than fade in. I'd like to have the entire mobject be on the screen just with 0 opacity
    #  So, fading in is misleading because it implies that it's not yet present on the screen.
    def fade_in_lines(self, *line_numbers: int) -> tuple[CustomCode, Animation]:
        copy = self._create_animation_copy()
        for line_no in line_numbers:
            copy.code[line_no].set_opacity(1)

        return copy, TransformSinglyLinkedList(self, copy)

    def fade_in_substring(self, substring: str, occurrence: int = 1) -> tuple[CustomCode, Animation]:
        copy = self._create_animation_copy()
        copy.get_code_substring(substring, occurrence=occurrence).set_opacity(1)
        return copy, TransformSinglyLinkedList(self, copy)

    def saturation_highlight_substring(self, substring: str, occurrence: int = 1) -> tuple[CustomCode, Animation]:
        copy = self._create_animation_copy()
        substring_start_index = self.get_substring_starting_index(substring, occurrence=occurrence)

        desaturate_opacity = 0.25
        copy.code.lines_text[:substring_start_index].set_opacity(desaturate_opacity)
        copy.code.lines_text[substring_start_index + len(substring) :].set_opacity(desaturate_opacity)

        return copy, TransformSinglyLinkedList(self, copy)

    def change_code_text(self, new_code_string: str) -> tuple[CustomCode, Animation]:
        copy = self._create_animation_copy()
        copy._original__init__(code=new_code_string)

        return CodeTransform(self, CustomCode(code=new_code_string))

    def get_substring_starting_index(self, substring: str, occurrence: int = 1, line_index: int | None = None) -> int:
        num_found: int = 0
        start_index: int = 0
        while True:
            start_index: int = self.code_string.find(substring, start_index)

            num_found += 1
            if num_found == occurrence:
                return start_index

            start_index += 1

    def get_code_substring(self, substring: str, occurrence: int = 1):
        start_index: int = self.get_substring_starting_index(substring, occurrence=occurrence)
        return self.code.lines_text[start_index : start_index + len(substring)]

    def get_line(self, line_number: int):
        return self.code[line_number - 1]

    def get_line_at(self, line_index: int):
        return self[2][line_index]

    def has_highlighter(self) -> bool:
        return self.highlighter is not None

    def create_highlighter(self):
        self.highlighter = CodeHighlighter(self)
        self.add(self.highlighter)
        return self.highlighter

    def move_highlighter(self, num_lines: int) -> None:
        return self.highlighter.move(num_lines)

    def move_highlighter_to_substring(self, substring: str, occurrence: int = 1, num_lines: int | None = None):
        return self.highlighter.move_to_substring(
            substring,
            occurrence=occurrence,
            num_lines=num_lines,
        )

    def set_background_color(self, color: str) -> None:
        self.background_mobject.set(color=color)

    def _create_animation_copy(self) -> CustomCode:
        attr_name = "_copy_for_animation"
        if not hasattr(self, attr_name):
            setattr(self, attr_name, self.copy())

        return getattr(self, attr_name)
