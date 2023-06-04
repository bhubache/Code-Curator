from manim import *

class ProblemText(Tex):
    def __init__(self, text, color = '#DBC9B8', **kwargs):
        super().__init__(text, color=color, tex_environment=r'\begin{tabular}{p{15 cm}}', **kwargs)

    @staticmethod
    def create_title(text, **kwargs):
        return ProblemText(text, **kwargs)

    @staticmethod
    def create_header(text, font_size = 40, color = '#337357', **kwargs):
        return ProblemText(text, font_size=font_size, color=color, **kwargs)

    @staticmethod
    def create_statement(text, font_size = 30, **kwargs):
        return ProblemText(text, font_size=font_size, **kwargs)

    @staticmethod
    def create_constraints_list(constraints, color='#DBC9B8', font_size = 25, dot_scale_factor = 1, buff = 0.25, **kwargs):
        bulleted_list = BulletedList(
            *[c for c in constraints],
            color=color,
            font_size=font_size,
            dot_scale_factor=dot_scale_factor,
            buff=buff
        )
        for bullet in bulleted_list:
            bullet.set_color(color)
        return bulleted_list

    @staticmethod
    def create_constraints_table(constraints, explanations, color = '#DBC9B8'):
        row_list = []
        for constraint, explanation in zip(constraints, explanations):
            row_list.append(
                [
                    ProblemText.create_statement(constraint),
                    ProblemText.create_statement(explanation, fill_opacity=0)
                ]
            )
        table = MobjectTable(row_list,
                             col_labels=[ProblemText.create_header('Constraint'),
                                         ProblemText.create_header('Explanation/Conclusion')],
                             include_outer_lines=True,
                             line_config={'color': color, 'stroke_width': 1.5}).scale(0.75)
        return table

    @staticmethod
    def create_key_points_table(points, explanations, color = '#DBC9B8'):
        row_list = []
        for point, explanation in zip(points, explanations):
            row_list.append(
                [
                    ProblemText.create_statement(point),
                    ProblemText.create_statement(explanation, fill_opacity=0)
                ]
            )
        table = MobjectTable(row_list,
                             col_labels=[ProblemText.create_header('Key Point'),
                                         ProblemText.create_header('Explanation/Conclusion')],
                             include_outer_lines=True,
                             line_config={'color': color, 'stroke_width': 1.5}).scale(0.75)
        return table