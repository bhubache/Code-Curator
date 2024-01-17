from __future__ import annotations

import re
from pathlib import Path

from manim import Animation
from manim import Code
from manim import ParsableManimColor
from manim import YELLOW
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from code_curator.animations.code_transform import CodeTransform
from code_curator.animations.singly_linked_list.transform_sll import TransformSinglyLinkedList
from code_curator.code.code_highlighter import CodeHighlighter
from code_curator.code.one_dark_colors import OneDarkStyle
from code_curator.code.python_lexer import MyPythonLexer
from code_curator.custom_vmobject import CustomVMobject


class CuratorCode(CustomVMobject):
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
        style: str = OneDarkStyle,
        language: str = "python",
        background_color: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__()
        self.lexer = MyPythonLexer()
        self.code_mobject = Code(
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
        self.add(self.code_mobject)

        self.background_mobject.set_opacity(0)
        self._highlighter = None

        self.scale(0.5)

    @property
    def code_string(self):
        return self.code_mobject.code_string

    @property
    def language(self):
        return self.code_mobject.language

    @property
    def style(self):
        return self.code_mobject.style

    @property
    def insert_line_no(self):
        return self.code_mobject.insert_line_no

    @property
    def file_path(self):
        return self.code_mobject.file_path

    @property
    def line_no_from(self):
        return self.code_mobject.line_no_from

    @property
    def generate_html_file(self):
        return self.code_mobject.generate_html_file

    @property
    def num_lines(self) -> int:
        return len(self.code_mobject.code)

    @property
    def background_mobject(self):
        return self.code_mobject.background_mobject

    @property
    def max_line_height(self):
        # Exclude whitespace from consideration
        max_height = float("-inf")
        for line_index, line_mobject in enumerate(self.code_mobject.code):
            tallest_reaching_amount: float = float("-inf")
            lowest_reaching_amount: float = float("inf")

            for char_index, char_mobject in enumerate(line_mobject):
                if self.code_mobject.code_string.splitlines()[line_index][char_index].isspace():
                    continue

                tallest_reaching_amount = max(tallest_reaching_amount, char_mobject.get_top()[1])
                lowest_reaching_amount = min(lowest_reaching_amount, char_mobject.get_bottom()[1])

            max_height = max(max_height, tallest_reaching_amount - lowest_reaching_amount)

        return max_height

    @property
    def max_line_width(self):
        # I want the max line width including the indentation chars at the beginning of a line
        min_starting_x = min(line.get_left()[0] for line in self.code_mobject.code)
        max_ending_x = max(line.get_right()[0] for line in self.code_mobject.code)
        return max_ending_x - min_starting_x

    @property
    def highlighter(self) -> CodeHighlighter:
        return self._highlighter

    @highlighter.setter
    def highlighter(self, highlighter: CodeHighlighter) -> None:
        self._highlighter = highlighter
        self._highlighter.code = self

    def fade_in_lines(self, *line_numbers: int) -> tuple[CuratorCode, Animation]:
        copy = self._create_animation_copy()
        for line_no in line_numbers:
            copy.code[line_no].set_opacity(1)

        return copy, TransformSinglyLinkedList(self, copy)

    def fade_in_substring(self, substring: str, occurrence: int = 1) -> tuple[CuratorCode, Animation]:
        copy = self._create_animation_copy()
        copy.get_code_substring(substring, occurrence=occurrence).set_opacity(1)
        return copy, TransformSinglyLinkedList(self, copy)

    def saturation_highlight_substring(self, substring: str, occurrence: int = 1) -> tuple[CuratorCode, Animation]:
        copy = self._create_animation_copy()
        substring_start_index = self.get_substring_starting_index(substring, occurrence=occurrence)

        desaturate_opacity = 0.25
        copy.code.lines_text[:substring_start_index].set_opacity(desaturate_opacity)
        copy.code.lines_text[substring_start_index + len(substring) :].set_opacity(desaturate_opacity)

        return copy, TransformSinglyLinkedList(self, copy)

    def change_code_text(self, new_code_string: str) -> tuple[CuratorCode, Animation]:
        copy = self._create_animation_copy()
        copy._original__init__(code=new_code_string)

        return CodeTransform(self, CuratorCode(code=new_code_string))

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
        return self.code_mobject.code.lines_text[start_index : start_index + len(substring)]

    def get_line(self, line_number: int):
        return self.code_mobject.code[line_number - 1]

    def has_highlighter(self) -> bool:
        return self.highlighter is not None

    def add_highlighter(self, start_line: int = 1, color: ParsableManimColor = YELLOW, opacity: float = 0.5):
        self.highlighter = CodeHighlighter(
            code=self,
            color=color,
            start_line=start_line,
            opacity=opacity,
        )
        self.add(self.highlighter)
        return self

    def move_highlighter_to_line(self, line_num: int) -> None:
        return self.highlighter.move_to_line(line_num)

    def move_highlighter_to_substring(self, substring: str, occurrence: int = 1, num_lines: int | None = None):
        return self.highlighter.move_to_substring(
            substring,
            occurrence=occurrence,
            num_lines=num_lines,
        )

    def set_background_color(self, color: str) -> None:
        self.code_mobject.background_mobject.set(color=color)

    def _create_animation_copy(self) -> CuratorCode:
        attr_name = "_copy_for_animation"
        if not hasattr(self, attr_name):
            setattr(self, attr_name, self.copy())

        return getattr(self, attr_name)

    def _gen_html_string(self):
        """Function to generate html string with code highlighted and stores in variable html_string."""
        self.html_string = _hilite_me(
            self.code_string,
            self.language,
            self.style,
            self.insert_line_no,
            "border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;",
            self.file_path,
            self.line_no_from,
            lexer=self.lexer,
        )

        if self.generate_html_file:
            output_folder = Path() / "assets" / "codes" / "generated_html_files"
            output_folder.mkdir(parents=True, exist_ok=True)
            (output_folder / f"{self.file_name}.html").write_text(self.html_string)


def _insert_line_numbers_in_html(html: str, line_no_from: int):
    """Function that inserts line numbers in the highlighted HTML code.

    Parameters
    ----------
    html
        html string of highlighted code.
    line_no_from
        Defines the first line's number in the line count.

    Returns
    -------
    :class:`str`
        The generated html string with having line numbers.
    """
    match = re.search("(<pre[^>]*>)(.*)(</pre>)", html, re.DOTALL)
    if not match:
        return html
    pre_open = match.group(1)
    pre = match.group(2)
    pre_close = match.group(3)

    html = html.replace(pre_close, "</pre></td></tr></table>")
    numbers = range(line_no_from, line_no_from + pre.count("\n") + 1)
    format_lines = "%" + str(len(str(numbers[-1]))) + "i"
    lines = "\n".join(format_lines % i for i in numbers)
    html = html.replace(
        pre_open,
        "<table><tr><td>" + pre_open + lines + "</pre></td><td>" + pre_open,
    )
    return html


def _hilite_me(
    code: str,
    language: str,
    style: str,
    insert_line_no: bool,
    divstyles: str,
    file_path: Path,
    line_no_from: int,
    lexer,
):
    """Function to highlight code from string to html.

    Parameters
    ---------
    code
        Code string.
    language
        The name of the programming language the given code was written in.
    style
        Code style name.
    insert_line_no
        Defines whether line numbers should be inserted in the html file.
    divstyles
        Some html css styles.
    file_path
        Path of code file.
    line_no_from
        Defines the first line's number in the line count.
    """
    style = style or "colorful"
    defstyles = "overflow:auto;width:auto;"

    formatter = HtmlFormatter(
        style=style,
        linenos=False,
        noclasses=True,
        cssclass="",
        cssstyles=defstyles + divstyles,
        prestyles="margin: 0",
    )
    if language is None and file_path:
        # lexer = guess_lexer_for_filename(file_path, code)
        html = highlight(code, lexer, formatter)
    elif language is None:
        raise ValueError(
            "The code language has to be specified when rendering a code string",
        )
    else:
        html = highlight(code, get_lexer_by_name(language, **{}), formatter)
    if insert_line_no:
        html = _insert_line_numbers_in_html(html, line_no_from)
    html = "<!-- HTML generated by Code() -->" + html
    return html
