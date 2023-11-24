from __future__ import annotations

import re
import difflib
import os

from manim import Code, BLACK, RED, YELLOW, BLUE, ORANGE, PURPLE, Rectangle, LEFT, UP, DOWN, RIGHT, AnimationGroup, FadeIn, FadeOut, Mobject
from manim import Animation

from .code_highlighter import CodeHighlighter
from code_curator.animations.singly_linked_list.transform_sll import TransformSinglyLinkedList

class CustomCode(Code):
    def __init__(
        self,
        file_name: str | None = None,
        tab_width: int = 1,
        indentation_chars: str = " ",
        margin: float = 0.1,
        background_stroke_width: float = 0,
        corner_radius: float = 0.0,
        insert_line_no: bool = False,
        line_no_buff: float = 0.2,
        style: str = 'nord',
        language: str = 'python',
        background_color: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            file_name=file_name,
            tab_width=tab_width,
            margin=margin,
            background_stroke_width=background_stroke_width,
            corner_radius=corner_radius,
            insert_line_no=insert_line_no,
            line_no_buff=line_no_buff,
            style=style,
            language=language,
            indentation_chars=indentation_chars,
            **kwargs,
        )
        self.background_mobject.set_opacity(0)
        # self.set_background_color(background_color)
        self._highlighter = None

    # TOOD: Give better name than fade in. I'd like to have the entire mobject be on the screen just with 0 opacity
    # So, fading in is misleading because it implies that it's not yet present on the screen.
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
        copy.code.lines_text[substring_start_index + len(substring):].set_opacity(desaturate_opacity)

        return copy, TransformSinglyLinkedList(self, copy)
    
    def change_code_text(self, new_code_string: str) -> tuple[CustomCode, Animation]:
        copy = self._create_animation_copy()
        copy._original__init__(code=new_code_string)
        # copy = CustomCode(code=new_code_string, language="java")
        # return copy, TransformSinglyLinkedList(self, copy)
        # code_with_new_text = self._original__init__(code=new_code_string)
        from code_curator.animations.code_transform import CodeTransform

        return CodeTransform(self, copy).get_animation()

    def get_substring_starting_index(self, substring: str, occurrence: int = 1) -> int:
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
        return self.code.lines_text[start_index: start_index + len(substring)]
    
    def _create_animation_copy(self) -> CustomCode:
        attr_name = "_copy_for_animation"
        if not hasattr(self, attr_name):
            setattr(self, attr_name, self.copy())

        return getattr(self, attr_name)

    def get_fade_out_animation(
        self,
        string: str | None = None,
        occurrence: int = 1,
    ) -> Animation:
        return FadeOut(self.get_substring_code(string, occurrence))

    def get_opacity_animation(
        self,
        string: str | None = None,
        occurrence: int = 1,
        opacity: float = 1.0,
    ) -> Animation:
        code_opacity_animation = self.get_substring_code(string, occurrence).animate.set_opacity(opacity)
        no_op_animation = Animation(Mobject())
        try:
            if self[0].fill_opacity == 1:
                background_opacity_animation = no_op_animation
            else:
                self[0].fill_opacity = 1
                background_opacity_animation = self[0].animate.set_opacity(1)
        except AttributeError:
            background_opacity_animation = no_op_animation

        return AnimationGroup(
            code_opacity_animation,
            background_opacity_animation,
        )

    @property
    def num_lines(self) -> int:
        return len(self.line_numbers)

    @property
    def highlighter(self) -> CodeHighlighter:
        return self._highlighter

    @highlighter.setter
    def highlighter(self, highlighter: CodeHighlighter) -> None:
        self._highlighter = highlighter
        self._highlighter.code = self

    def get_line(self, line_number: int):
        return self.code[line_number - 1]

    def get_token_at_line(self, token: str, line_num: int, occurrence: int):
        start_index, end_index = None, None
        for i, line in enumerate(self.code_string.splitlines()):
            if i == line_num:
                token_start_index = line.find(token)
                for i in range(occurrence - 1):
                    token_start_index = line.find(token, token_start_index + 1)

                match = re.search(pattern=token, string=line[token_start_index:])

                if match is None:
                    raise RuntimeError(f'Unable to find occurrence {occurrence} of token {token} in line {line}')

                start_index = token_start_index
                end_index = match.end() + token_start_index
                break
        return self.get_line_at(line_num)[start_index : end_index]

    def has_highlighter(self) -> bool:
        return self.highlighter is not None

    def create_highlighter(self, color = YELLOW):
        self.highlighter = CodeHighlighter(self)
        return self.highlighter

    def move_highlighter(self, num_lines: int) -> None:
        return self.highlighter.move(num_lines)

    def move_highlighter_to_token(self, token: str, occurrence: int, num_lines: int = 0):
        line_move_animation = self.move_highlighter(num_lines=num_lines)
        token_move_animation = self.highlighter.move_to_token(token, occurrence=occurrence)
        return AnimationGroup(line_move_animation, token_move_animation)

    @property
    def line_height(self):
        max_height = 0
        for line in self.code:
            max_height = max(max_height, line.height)

        return max_height

    @property
    def line_width(self):
        max_width = 0
        for line in self.code:
            max_width = max(max_width, line.width)

        return max_width

    def has_more_height(self, other):
        return self.height >= other.height

    def has_more_width(self, other):
        return self.width >= other.width

    def set_background_color(self, color: str) -> None:
        self.background_mobject.set(color=color)
