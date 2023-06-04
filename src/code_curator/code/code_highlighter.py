from __future__ import annotations

from manim import AnimationGroup
from manim import Code
from manim import DOWN
from manim import LEFT
from manim import Rectangle
from manim import YELLOW


class CodeHighlighter(Rectangle):
    def __init__(self, code: Code, height: float = None, width: float = None, color=YELLOW, stroke_width=0):
        self._custom_init_super(
            code=code, height=height, width=width, color=color, stroke_width=stroke_width,
        )

    @property
    def code(self) -> Code:
        return self._code

    @code.setter
    def code(self, new_code: Code) -> None:
        self._code = new_code

    @property
    def curr_line_num(self) -> int:
        return self._curr_line_num

    @curr_line_num.setter
    def curr_line_num(self, new_line_num: int) -> None:
        self._curr_line_num = new_line_num

    def _custom_init_super(self, code, height, width, color, stroke_width):
        if height is None:
            height = code.line_height + 0.05
        if width is None:
            width = code.line_width + 0.1

        super().__init__(height=height, width=width, color=color, stroke_width=stroke_width)

        self._code = code
        self._curr_line_num = 0
        self.set_opacity(0.5)
        self.align_to(self.code[2][self._curr_line_num], DOWN)
        self.align_to(self.code[2][self._curr_line_num], LEFT)

    def move_to_token(self, token: str, occurrence: int = 1):
        '''
        For the line the highlighter is on, you can specify a token for the
        highlighter to cover
        '''
        code_token_obj = self.code.get_token_at_line(
            token=token, line_num=self.curr_line_num, occurrence=occurrence,
        )
        return AnimationGroup(
            AnimationGroup(
                self.animate.become(
                    CodeHighlighter(
                        code=self.code,
                        width=code_token_obj.width,
                    ).align_to(self.code.get_line_at(self.curr_line_num), DOWN)
                    .align_to(code_token_obj, LEFT),
                ),
            ),
        )

    def move(self, num_lines: int) -> None:
        new_line_num = self.curr_line_num + num_lines
        if new_line_num < 0 or new_line_num >= self.code.num_lines:
            raise IndexError(
                f'{new_line_num} is out of bounds for {self.code.num_lines}',
            )

        self.curr_line_num = new_line_num

        return self.animate.become(CodeHighlighter(self.code).align_to(self.code[2][new_line_num], DOWN))
