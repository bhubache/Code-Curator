from __future__ import annotations

from typing import TYPE_CHECKING

from manim import BulletedList
from manim import MobjectTable
from manim import Tex

from code_curator._utils.string import partition


if TYPE_CHECKING:
    from collections.abc import Sequence


# TODO: Have title cover full width of screen regarless of font size


class ProblemText(Tex):
    def __init__(
        self,
        text,
        color: str = '#DBC9B8',
        **kwargs,
    ) -> None:
        # self.text_strings = text.split()
        # self.tex_pieces: list[Tex] = [Tex(word, color=color, **kwargs) for word in text.split()]
        super().__init__(*text.split(), arg_separator=' ', color=color, tex_environment=r'\begin{tabular}{p{15 cm}}', **kwargs)
        # super().__init__(text, color=color, tex_environment=r'\begin{tabular}{p{15 cm}}', **kwargs)

    @staticmethod
    def create_title(text: str, **kwargs) -> ProblemText:
        return ProblemText(text, **kwargs)

    @staticmethod
    def create_header(text: str, font_size: int = 40, color: str = '#337357', **kwargs) -> ProblemText:
        return ProblemText(text, font_size=font_size, color=color, **kwargs)

    @staticmethod
    def create_statement(text: str, font_size: int = 30, **kwargs) -> ProblemText:
        return ProblemText(text, font_size=font_size, **kwargs)

    @staticmethod
    def create_constraints_list(
        constraints: Sequence[str],
        color: str = '#DBC9B8',
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
    def create_constraints_table(
        constraints: Sequence[str],
        explanations: Sequence[str],
        color: str = '#DBC9B8',
    ) -> MobjectTable:
        row_list = []
        for constraint, explanation in zip(constraints, explanations):
            row_list.append(
                [
                    ProblemText.create_statement(constraint),
                    ProblemText.create_statement(explanation, fill_opacity=0),
                ],
            )

        return MobjectTable(
            row_list,
            col_labels=[
                ProblemText.create_header('Constraint'),
                ProblemText.create_header('Explanation/Conclusion'),
            ],
            include_outer_lines=True,
            line_config={'color': color, 'stroke_width': 1.5},
        ).scale(0.75)

    @staticmethod
    def create_key_points_table(
        points: Sequence[str],
        explanations: Sequence[str],
        color: str = '#DBC9B8',
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
                ProblemText.create_header('Key Point'),
                ProblemText.create_header('Explanation/Conclusion'),
            ],
            include_outer_lines=True,
            line_config={'color': color, 'stroke_width': 1.5},
        ).scale(0.75)

    def get_sub_tex(self, substring: str):
        text_partition = partition(' '.join(self.tex_strings), substring)
        start_index = len(text_partition[0].split())
        end_index = start_index + len(text_partition[1].split())
        return self[start_index : end_index]
