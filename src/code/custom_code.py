import re
import difflib
import os

from manim import Code, BLACK, RED, YELLOW, BLUE, ORANGE, PURPLE, Rectangle, LEFT, UP, DOWN, AnimationGroup

from .code_highlighter import CodeHighlighter

class CustomCode(Code):
    def __init__(
        self,
        file_name: str,
        tab_width = 4,
        font='Monospace',
        font_size = 24,
        background_stroke_width: float = 0,
        background_color = BLACK,
        insert_line_no: bool = False,
        style: str = 'nord',
        language: str = 'java',
        **kwargs):
        self._make_blank_lines_not_empty(file_name)

        super().__init__(
            file_name=file_name,
            tab_width=tab_width,
            font=font,
            font_size=font_size,
            background_stroke_width=background_stroke_width,
            insert_line_no=insert_line_no,
            style=style,
            language=language,
            **kwargs
        )
        self._set_background_color(background_color)
        self._highlighter = None

    @property
    def num_lines(self) -> int:
        return len(self[2])

    @property
    def highlighter(self) -> CodeHighlighter:
        return self._highlighter

    @highlighter.setter
    def highlighter(self, highlighter: CodeHighlighter) -> None:
        self._highlighter = highlighter
        self._highlighter.code = self

    def get_line_at(self, line_index: int):
        return self[2][line_index]

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

    def _make_blank_lines_not_empty(self, file_path: str) -> None:
        contents = None
        with open(file_path, 'r') as read_file:
            contents = read_file.read()

        content_lines = contents.splitlines()
        for i, line in enumerate(content_lines):
            if line.strip() == '':
                content_lines[i] = ' '

        no_blank_lines_contents = '\n'.join(content_lines)
        

        with open(file_path, 'w') as write_file:
            write_file.write(no_blank_lines_contents)

    @property
    def line_height(self):
        return CustomCode(file_name=os.path.join(os.getcwd(), 'src/code/helper_files/line_height.java'))[2][0].height
        # return self.submobjects[2][0].height

    @property
    def line_width(self):
        max_width = 0
        for line in self.submobjects[2]:
            if line.width > max_width:
                max_width = line.width
        return max_width


    def has_more_height(self, other):
        return self.height >= other.height

    def has_more_width(self, other):
        return self.width >= other.width

    def _set_background_color(self, color: str) -> None:
        self.submobjects[0].set_color(color)