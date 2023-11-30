from __future__ import annotations

from typing import TYPE_CHECKING

from manim import BulletedList
from manim import config
from manim import Group
from manim import LEFT
from manim import MobjectTable
from manim import RIGHT
from manim import Tex
from manim import TexTemplate
from manim import UP

from code_curator._utils.string import partition
from code_curator.constants import DEFAULT_MOBJECT_COLOR


if TYPE_CHECKING:
    from collections.abc import Sequence


# TODO: Have title cover full width of screen regarless of font size


class ProblemText(Tex):
    def __init__(
        self,
        text,
        color: str = "#DBC9B8",
        **kwargs,
    ) -> None:
        my_template = TexTemplate()
        my_template.add_to_preamble(r"\usepackage[most]{tcolorbox}")
        my_template.add_to_preamble(
            r"\tcbset{on line, boxsep=2pt, left=0pt,right=0pt,top=0pt,bottom=0pt, frame hidden,"
            r" colframe=white,colback=white, highlight math style={enhanced}}",
        )
        my_template.add_to_preamble(r"\newcommand{\code}[1]{\tcbox{\texttt{#1}}}")
        super().__init__(
            *text.split(),
            arg_separator=" ",
            color=color,
            tex_environment=r"\begin{tabular}{p{17.5 cm}}",
            tex_template=my_template,
            **kwargs,
        )

        for word_tex in self:
            if word_tex.tex_string.startswith("\\code"):
                # NOTE: Assuming that the background mobject is the second submobject

                word_tex.submobjects[0].set(color=config["background_color"])
                word_tex.submobjects[1].set(color="#808080")

                class StaticColorWrapper(type(word_tex.submobjects[0])):
                    def __init__(self, mobject) -> None:
                        self.mobject = mobject

                    def __getattr__(self, item):
                        result = getattr(self.mobject, item)
                        if result is self.mobject:
                            return self

                        return result

                    def set_fill(
                        self,
                        color=None,
                        opacity=None,
                        family: bool = True,
                    ):
                        # TODO: Figure out why simple delegation doesn't work
                        color = self.fill_color
                        if family:
                            for submobject in self.submobjects:
                                submobject.set_fill(color, opacity, family)
                        self.update_rgbas_array("fill_rgbas", color, opacity)
                        self.fill_rgbas: RGBA_Array_Float
                        if opacity is not None:
                            self.fill_opacity = opacity
                        return self

                word_tex.submobjects[0] = StaticColorWrapper(word_tex.submobjects[0])
                word_tex.submobjects[1] = StaticColorWrapper(word_tex.submobjects[1])

    def set_color(self, color, family=True):
        for word_tex in self:
            if word_tex.tex_string.startswith("\\code"):
                # NOTE: Assuming that the background mobject is the second submobject
                word_tex.submobjects[0].set(color=config["background_color"])
                word_tex.submobjects[1].set(color="#808080")

    @staticmethod
    def create_title(text: str, **kwargs) -> ProblemText:
        return ProblemText(text, **kwargs)

    @staticmethod
    def create_header(text: str, font_size: int = 40, color: str = "#337357", **kwargs) -> ProblemText:
        return ProblemText(text, font_size=font_size, color=color, **kwargs)

    @staticmethod
    def create_statement(text: str, font_size: int = 30, **kwargs) -> ProblemText:
        return ProblemText(text, font_size=font_size, **kwargs)

    @staticmethod
    def create_tex(
        text: str,
        font_size: int = 30,
        color: str = DEFAULT_MOBJECT_COLOR,
        **kwargs,
    ) -> Tex:
        tex_strings: list[str] = []
        latex_math_mode_started = False
        for char in text:
            if char == "$":
                latex_math_mode_started = not latex_math_mode_started
                if latex_math_mode_started:
                    tex_strings.append("")
                else:
                    tex_strings[-1] += char
                    continue

            if latex_math_mode_started:
                tex_strings[-1] += char
            else:
                tex_strings.append(char)

        return Tex(
            # *tex_strings,
            *text.split(),
            font_size=font_size,
            color=color,
            arg_separator=" ",
            **kwargs,
        )

    @staticmethod
    def create_list(
        *list_items,
        preamble: str = "",
        color: str = DEFAULT_MOBJECT_COLOR,
        font_size: int = 20,
        dot_scale_factor: int = 1,
        vertical_buff: float = 0.25,
        horizontal_buff: float = 0.25,
    ) -> BulletedList | Group:
        bulleted_list = BulletedList(
            *list_items,
            color=color,
            font_size=font_size,
            dot_scale_factor=dot_scale_factor,
            buff=vertical_buff,
        )

        for bullet in bulleted_list:
            # Cut of the sequence of backslashes at the end
            bullet.tex_string = bullet.tex_string[:-2]
            bullet.set_color(color)

        if preamble:
            preamble_tex = ProblemText.create_tex(
                preamble,
                font_size=font_size,
            )
            preamble_tex.next_to(bulleted_list, UP)
            bulleted_list.align_to(preamble_tex, LEFT)
            bulleted_list.shift(RIGHT * horizontal_buff)
            group = Group(
                preamble_tex,
                bulleted_list,
            )
            return group

        return bulleted_list

    @staticmethod
    def create_constraints_list(
        constraints: Sequence[str],
        color: str = "#DBC9B8",
        font_size: int = 25,
        dot_scale_factor: int = 1,
        buff: float = 0.25,
        **kwargs,
    ) -> BulletedList:
        bulleted_list = BulletedList(
            *constraints,
            color=color,
            font_size=font_size,
            dot_scale_factor=dot_scale_factor,
            buff=buff,
        )
        for bullet in bulleted_list:
            bullet.set_color(color)

        return bulleted_list

    @staticmethod
    def create_table(
        first_column_entries: Sequence[str],
        second_column_entries: Sequence[str],
        *,
        row_headers: Sequence[str],
        columns_to_hide: Sequence[int] = (),
        color: str = DEFAULT_MOBJECT_COLOR,
    ) -> MobjectTable:
        rows = []
        for left_entry, right_entry in zip(first_column_entries, second_column_entries):
            rows.append(
                [
                    ProblemText.create_tex(left_entry),
                    ProblemText.create_tex(right_entry),
                ],
            )

        for row in rows:
            for column in columns_to_hide:
                row[column].set_opacity(0)

        return MobjectTable(
            rows,
            col_labels=[ProblemText.create_header(header) for header in row_headers],
            include_outer_lines=True,
            line_config={"color": color, "stroke_width": 1.5},
        )

    @staticmethod
    def create_constraints_table(
        constraints: Sequence[str],
        explanations: Sequence[str],
        color: str = "#DBC9B8",
    ) -> MobjectTable:
        row_list = []
        for constraint, explanation in zip(constraints, explanations):
            row_list.append(
                [
                    ProblemText.create_tex(constraint),
                    ProblemText.create_tex(explanation, fill_opacity=0),
                ],
            )

        return MobjectTable(
            row_list,
            col_labels=[
                ProblemText.create_header("Constraint"),
                ProblemText.create_header("Explanation/Conclusion"),
            ],
            include_outer_lines=True,
            line_config={"color": color, "stroke_width": 1.5},
        ).scale(0.75)

    @staticmethod
    def create_key_points_table(
        points: Sequence[str],
        explanations: Sequence[str],
        color: str = "#DBC9B8",
    ) -> MobjectTable:
        row_list = []
        for point, explanation in zip(points, explanations):
            row_list.append(
                [
                    ProblemText.create_statement(point),
                    ProblemText.create_statement(explanation, fill_opacity=0),
                ],
            )

        return MobjectTable(
            row_list,
            col_labels=[
                ProblemText.create_header("Key Point"),
                ProblemText.create_header("Explanation/Conclusion"),
            ],
            include_outer_lines=True,
            line_config={"color": color, "stroke_width": 1.5},
        ).scale(0.75)

    def get_sub_tex(self, substring: str):
        text_partition = partition(" ".join(self.tex_strings), substring)
        start_index = len(text_partition[0].split())
        end_index = start_index + len(text_partition[1].split())
        sub_tex = self[start_index:end_index]
        sub_tex.problem_tex_parent = self
        return sub_tex
