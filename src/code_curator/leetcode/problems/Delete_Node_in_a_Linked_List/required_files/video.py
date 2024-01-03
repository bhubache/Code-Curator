from __future__ import annotations

from manim import AnimationGroup
from manim import config
from manim import DOWN
from manim import FadeIn
from manim import FadeOut
from manim import LEFT
from manim import Line
from manim import Rectangle
from manim import RIGHT
from manim import UP
from manim import VGroup
from manim import Wait
from manim import Write
from manim import YELLOW

from code_curator.animations.arrow_transport_transformation import ArrowTransportTransformation
from code_curator.animations.sliding_text_highlighter import SlidingTextHighlighter
from code_curator.animations.change_color import ChangeColor
from code_curator.animations.utils.utils import run_time_can_be_truncated
from code_curator.base_scene import BaseScene
from code_curator.data_structures.singly_linked_list_v2 import SinglyLinkedList
from code_curator.leetcode.problem_text import ProblemText
from code_curator.leetcode.scenes.present_problem.base_present_problem import BasePresentProblem as PresentProblem
from code_curator.leetcode.scenes.problem_analysis.base_problem_analysis import BaseProblemAnalysis as ProblemAnalysis
from code_curator.main import QUALITY

# from code_curator.data_structures.singly_linked_list import SinglyLinkedList

# TODO: Try and just have the special Mobject in curator animation be in the scene.mobjects
# TODO: Consider substrings_to_isolate when creating Tex for TransformMatchingTex


TITLE = "Delete Node in a Linked List"
STATEMENT = (
    r"There is a singly-linked list \code{head} and we want to delete a node \code{node} in it. You"
    r" are given the node to be deleted \code{node}. You will \textbf{not be given access} to the first"
    r" node of \code{head}. All the values of the linked list are \textbf{unique}, and it is guaranteed"
    r" that the given node \code{node} is not the last node in the linked list. Delete the"
    r" given node. Note that by deleting the node, we do not mean removing it from"
    r" memory. We mean:"
)

SPECIAL_NOTES = [
    "The value of the given node should not exist in the linked list",
    "The number of nodes in the linked list should decrease by one",
    "All the values before node should be in the same order",
    "All the values after node should be in the same order",
]

CONSTRAINTS = [
    "The number of nodes in the given list is in the range [2, 1000]",
    r"-1000 $\leq$ Node.val $\leq$ 1000",
    "The value of each node in the list is unique",
    "The node to be deleted is in the list and is not a tail node",
]

CONSTRAINT_EXPLANATIONS = [
    "Node is in the list and is not the tail node",
    "Solution may involve arithmetic",
    "Not pertinent",
    "It's impossible to delete the tail",
]

REMOVE_COLOR = "#FF0000"
KEEP_COLOR = "#00FF00"
RESET_COLOR = "#DBC9B8"
STATEMENT_FONT_SIZE = 25


class Video(BaseScene):
    config["quality"] = QUALITY

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title_tex = ProblemText.create_title(TITLE)
        self.statement_header_tex = ProblemText.create_header("Statement")

        # TODO: Make the left and right margins equal
        self.statement_tex = ProblemText.create_statement(STATEMENT, font_size=STATEMENT_FONT_SIZE)
        self.special_notes_list = ProblemText.create_list(*SPECIAL_NOTES).scale(0.75)
        self.constraints_header_tex = ProblemText.create_header("Constraints")
        self.constraints_list = ProblemText.create_list(*CONSTRAINTS)

        self.notes_title = ProblemText.create_header("Notes").scale(0.75)
        self.notes_surrounding_rectangle = Rectangle(
            height=self.camera.frame_height,
            width=self.camera.frame_width,
        )
        self.notes_list = ProblemText.create_list(
            *(
                "Given the node to be deleted rather than the head of the linked list",
                "All values are unique",
                "Given node will not be the last node of the linked list",
                "You don't have to remove the node from memory: see bullet points",
                "The linked list will contain at least two nodes",
            ),
            vertical_buff=0.5,
        )

        self.first_tex_to_remove = self.statement_tex[37:64]
        self.first_mention_tex = self.statement_tex[10:16]
        self.second_mention_tex = self.statement_tex.get_sub_tex(
            "Delete the given node.",
        )

        self.constraints_analysis_title_tex = ProblemText.create_title("Constraints Analysis")
        self.constraints_analysis_table = ProblemText.create_constraints_table(
            constraints=CONSTRAINTS,
            explanations=CONSTRAINT_EXPLANATIONS,
        )

    def fade_in_title(self):
        return FadeIn(self.title_tex)

    def move_title(self):
        # TODO: Make movement smooth
        return self.title_tex.animate.to_edge(UP)

    def fade_in_statement_header(self):
        title_copy = self.title_tex.copy().to_edge(UP)
        self.statement_header_tex.next_to(title_copy, DOWN)
        self.statement_header_tex.to_edge(LEFT)
        return FadeIn(self.statement_header_tex)

    def fade_in_statement(self):
        self.statement_tex.next_to(self.statement_header_tex, DOWN)
        self.statement_tex.to_edge(LEFT)
        return FadeIn(self.statement_tex)

    def highlight_first_key_point(self):
        return SlidingTextHighlighter(self.statement_tex[18:35])
        # starting_rectangle = Rectangle(
        #     color=YELLOW,
        #     height=self.statement_tex.height,
        #     width=0,
        #     fill_color=YELLOW,
        #     fill_opacity=0.5,
        #     stroke_width=0
        # ).align_to(self.statement_tex[20], LEFT)

        # # ending_rectangle = starting_rectangle.copy().stretch_to_fit_width(3)
        # # ending_rectangle = Rectangle()

        # ending_rectangle = Rectangle(
        #     color=YELLOW,
        #     height=self.statement_tex.height,
        #     width=3,
        #     fill_color=YELLOW,
        #     fill_opacity=0.5,
        #     stroke_width=0,
        # ).align_to(self.statement_tex[20], LEFT)

        # self.add(starting_rectangle)

        # return starting_rectangle.animate.become(ending_rectangle)

    def fade_in_first_note(self):
        self.add(self.notes_list)
        self.notes_list.set_opacity(0)

        self.notes_surrounding_rectangle.next_to(self.statement_tex, DOWN)
        self.notes_surrounding_rectangle.shift((self.camera.frame_width / 2) * RIGHT)
        self.notes_title.next_to(self.notes_surrounding_rectangle.get_top(), DOWN)

        self.notes_title.align_on_border(RIGHT, buff=(self.notes_title.get_left()[0] - self.notes_title.get_right()[0]))
        self.notes_title.shift((self.notes_title.get_center() - self.notes_surrounding_rectangle.get_left()) / 2 * LEFT)

        self.notes_list.next_to(self.notes_title, DOWN).align_to(self.notes_surrounding_rectangle, LEFT).shift(RIGHT * 0.1)


        return FadeIn(self.notes_title, self.notes_surrounding_rectangle), self.notes_list[0].animate.set_opacity(1)

    def deleting_point_1(self):
        self.special_notes_list.next_to(self.statement_tex, DOWN)
        self.special_notes_list.to_edge(LEFT)
        return FadeIn(self.special_notes_list[0])

    def deleting_point_2(self):
        return FadeIn(self.special_notes_list[1])

    def deleting_point_3(self):
        return FadeIn(self.special_notes_list[2])

    def deleting_point_4(self):
        return FadeIn(self.special_notes_list[3])

    def fade_in_constraints_header(self):
        self.constraints_header_tex.next_to(self.special_notes_list, DOWN)
        self.constraints_header_tex.to_edge(LEFT)
        return FadeIn(self.constraints_header_tex)

    def fade_in_constraint_one(self):
        self.constraints_list.next_to(self.constraints_header_tex, DOWN)
        self.constraints_list.to_edge(LEFT)
        return FadeIn(self.constraints_list[0])

    def fade_in_constraint_two(self):
        return FadeIn(self.constraints_list[1])

    def fade_in_constraint_three(self):
        return FadeIn(self.constraints_list[2])

    def fade_in_constraint_four(self):
        return FadeIn(self.constraints_list[3])

    def highlight_constraints_duplication(self):
        return AnimationGroup(
            ChangeColor(self.constraints_list[2], KEEP_COLOR),
            ChangeColor(self.constraints_list[3], KEEP_COLOR),
            ChangeColor(
                self.first_tex_to_remove,
                REMOVE_COLOR,
                starting_color=self.statement_tex.color,
            ),
        )

    def remove_constraints_duplication(self):
        return AnimationGroup(
            self.first_tex_to_remove.animate.set_opacity(0),
            ChangeColor(self.constraints_list[2], RESET_COLOR),
            ChangeColor(self.constraints_list[3], RESET_COLOR),
        )

    def highlight_statement_duplication(self):
        return AnimationGroup(
            ChangeColor(
                self.first_mention_tex,
                KEEP_COLOR,
                starting_color=self.statement_tex.color,
            ),
            ChangeColor(
                self.second_mention_tex,
                REMOVE_COLOR,
                starting_color=self.statement_tex.color,
            ),
        )

    def remove_statement_duplication(self):
        return AnimationGroup(
            self.second_mention_tex.animate.set_opacity(0),
            ChangeColor(self.first_mention_tex, RESET_COLOR),
        )

    def smooth_over_wording(self):
        new_statement_tex = ProblemText.create_statement(
            r"There is a singly linked list called \code{head} and a node that we wish to"
            r" remove called \code{node}. You will not be given access to the head of the"
            " list. Instead, you will be given access to the node to be deleted.",
            font_size=STATEMENT_FONT_SIZE,
        )
        new_statement_tex.next_to(self.statement_header_tex, DOWN)
        new_statement_tex.to_edge(LEFT)

        return FadeOut(self.statement_tex), FadeOut(self.first_mention_tex), FadeIn(new_statement_tex)

    def transition_to_constraints_analysis(self):
        return Wait()
        self.constraints_analysis_title_tex.to_edge(UP)

        # FIXME: This is for development, REMOVE THIS FOR PRODUCTION
        self.mobjects[0].add(self.title_tex)

        return (
            FadeOut(*self.scene_mobjects),
            FadeIn(self.constraints_analysis_title_tex),
            FadeIn(self.constraints_analysis_table),
        )

    def start_first_constraint_explanation(self):
        return Wait()
        self.fourth_constraint_table_breakdown = ProblemText.create_table(
            [
                "The node to be deleted is in the list",
                "The node to be deleted is not a tail node",
            ],
            [
                r"$\checkmark$",
                r"$\checkmark$",
            ],
            row_headers=[
                "Constraint Component",
                "Requirement Met",
            ],
            columns_to_hide=[1],
        ).scale(0.4)

        self.first_requirement = self.fourth_constraint_table_breakdown.get_columns()[1][1]
        self.second_requirement = self.fourth_constraint_table_breakdown.get_columns()[1][2]

        self.first_requirement.set_opacity(0)
        self.second_requirement.set_opacity(0)
        self.fourth_constraint_table_breakdown.to_edge(UP + LEFT)

        constraint_four_copy = self.constraints_analysis_table.get_columns()[0][4].copy()
        # self.mobjects[0].add(constraint_four_copy)
        self.constraints_analysis_table.get_columns()[0][4].set_stroke_opacity(0)
        self.constraints_analysis_table.get_columns()[0][4].set_opacity(0)
        return (
            ArrowTransportTransformation(
                constraint_four_copy,
                self.fourth_constraint_table_breakdown,
            ),
            FadeOut(self.constraints_analysis_title_tex),
            FadeOut(self.constraints_analysis_table),
        )

    def fade_in_node(self):
        # from code_curator.data_structures.graph import Edge
        # from code_curator.data_structures.graph import Vertex

        # vertex_one = Vertex(
        #     label=1,
        #     position=(-1.0, 0.0, 0.0),
        # )
        # vertex_two = Vertex(
        #     label=2,
        #     position=(1.0, 1.0, 0.0),
        # )
        # self.add(vertex_one)
        # self.add(vertex_two)
        # return FadeIn(
        #     Edge(
        #         vertex_one,
        #         vertex_two,
        #         directedness="->",
        #     )
        # )
        self.sll = SinglyLinkedList(0, 1, 2).add_null().add_head_pointer()
        # self.sll.head_pointer.set_opacity(0)
        # self.sll.tail_pointer.set_opacity(0)
        return FadeIn(self.sll)

    def fade_in_head(self):
        # return self.sll.animate.insert_node(1, 10)
        return self.sll.animate.move_labeled_pointer(self.sll.head_pointer, self.sll.get_node(1))
        # return self.sll.animate.insert_node(1, 10)
        return Wait()
        return self.sll.animate.insert_node(0, 10)
        return Wait()
        return self.sll.head_pointer.animate(run_time=0.3).set_opacity(1)

    # TODO: Try and make animations not interrupt each other
    def fade_in_tail(self):
        return Wait()
        return self.sll.tail_pointer.animate(run_time=0.3).set_opacity(1)

    def add_second_node(self):
        return self.sll.animate.move_to([1, 1, 0])
        return Wait()
        self.sll, animation = self.sll.insert_node(-1, 1)
        return animation


class PrimaryStream:
    def __init__(
        self,
        present_problem: PresentProblem,
        special_notes_list,
        problem_analysis: ProblemAnalysis,
        scene: BaseScene,
        shared,
        **kwargs,
    ) -> None:
        self.present_problem = present_problem
        self.special_notes_list = special_notes_list
        self.problem_analysis = problem_analysis
        self.scene = scene
        self.shared = shared

        self.tex_to_remove = self.present_problem.statement_tex.get_sub_tex(
            " All the values of the linked list are unique, and it is"
            " guaranteed that the given node node is not the last node in the"
            " linked list.",
        )
        self.third_constraint_tex = self.get_constraint_tex(3)
        self.fourth_constraint_tex = self.get_constraint_tex(4)

        self.first_mention_tex = self.present_problem.statement_tex.get_sub_tex(
            "delete a node node in it.",
        )
        self.second_mention_tex = self.present_problem.statement_tex.get_sub_tex(
            "Delete the given node.",
        )

        # self.first_mention_tex = self.statement.

    def __getattr__(self, name: str):
        return getattr(self.present_problem, name)

    @run_time_can_be_truncated
    def statement(self):
        animation = self.present_problem.statement()
        self.present_problem._position_element_below_other(self.statement_tex, self.statement_header_tex)
        return animation

    def deleting_point_1(self):
        self.present_problem._position_element_below_lowest_in_scene(self.special_notes_list)
        return FadeIn(self.special_notes_list[0])

    def deleting_point_2(self):
        return FadeIn(self.special_notes_list[1])

    def deleting_point_3(self):
        return FadeIn(self.special_notes_list[2])

    def deleting_point_4(self):
        return FadeIn(self.special_notes_list[3])

    def highlight_constraints_duplication(self):
        return AnimationGroup(
            ChangeColor(self.third_constraint_tex, KEEP_COLOR),
            ChangeColor(self.fourth_constraint_tex, KEEP_COLOR),
            ChangeColor(
                self.tex_to_remove,
                REMOVE_COLOR,
                starting_color=self.present_problem.statement_tex.color,
            ),
        )

    def remove_constraints_duplication(self):
        return AnimationGroup(
            # FadeOut(self.tex_to_remove),
            self.tex_to_remove.animate.set_opacity(0),
            ChangeColor(self.third_constraint_tex, RESET_COLOR),
            ChangeColor(self.fourth_constraint_tex, RESET_COLOR),
        )

    def highlight_statement_duplication(self):
        return AnimationGroup(
            ChangeColor(
                self.first_mention_tex,
                KEEP_COLOR,
                starting_color=self.present_problem.statement_tex.color,
            ),
            ChangeColor(
                self.second_mention_tex,
                REMOVE_COLOR,
                starting_color=self.present_problem.statement_tex.color,
            ),
        )

    def remove_statement_duplication(self):
        return AnimationGroup(
            # FadeOut(self.second_mention_tex),
            self.second_mention_tex.animate.set_opacity(0),
            ChangeColor(self.first_mention_tex, RESET_COLOR),
        )

    def smooth_over_wording(self):
        # new_statement = self._create_statement(
        #     "There is a singly linked list called head and a node that we wish to"
        #     " remove called node. You will not be given access to the head of the"
        #     " list. Instead, you will be given access to the node to be deleted.",
        # )
        # self.present_problem._position_element_below_other(new_statement, self.present_problem.statement_header_tex)
        # TODO: Introducer not working for animations that are part of AnimationGroup
        return AnimationGroup(
            FadeOut(self.present_problem.statement_tex),
            # FadeIn(new_statement),
        )

    def start_first_constraint_explanation(self):
        self.fourth_constraint_table_breakdown = ProblemText.create_table(
            [
                "The node to be deleted is in the list",
                "The node to be deleted is not a tail node",
            ],
            [
                r"$\checkmark$",
                r"$\checkmark$",
            ],
            row_headers=[
                "Constraint Component",
                "Requirement Met",
            ],
            columns_to_hide=[1],
        ).scale(0.4)
        self.shared.first_requirement = self.fourth_constraint_table_breakdown.get_columns()[1][1]
        self.shared.second_requirement = self.fourth_constraint_table_breakdown.get_columns()[1][2]
        self.shared.first_requirement.set_opacity(0)
        self.shared.second_requirement.set_opacity(0)
        # self.fourth_constraint_table_breakdown.get_cell((1, 1)).set_opacity(0)
        # self.fourth_constraint_table_breakdown.get_cell((2, 1)).set_opacity(0)
        self.fourth_constraint_table_breakdown.to_edge(UP + LEFT)

        constraint_four_copy = self.problem_analysis.get_constraint_tex(4).copy()
        self.problem_analysis.get_constraint_tex(4).set_stroke_opacity(0)
        self.problem_analysis.get_constraint_tex(4).set_opacity(0)
        return ArrowTransportTransformation(
            constraint_four_copy,
            self.fourth_constraint_table_breakdown,
        )

    def fade_in_node(self):
        self.sll = SinglyLinkedList(0)
        # self.sll.head_pointer.set_opacity(0)
        # self.sll.tail_pointer.set_opacity(0)
        return FadeIn(self.sll)

    def fade_in_head(self):
        return self.sll.head_pointer.animate(run_time=0.3).set_opacity(1)

    def fade_in_tail(self):
        return Wait()
        # return self.sll.tail_pointer.animate(run_time=0.3).set_opacity(1)

    def add_second_node(self):
        return (
            self.sll.add_last(data=1)
            .subsequently_fade_in_container()
            .with_fade_in_pointer()
            .with_center_sll()
            .with_move_tail()
            .build()
        )

    def fade_in_constraints_table(self):
        return FadeIn(
            self.problem_analysis.title_tex,
            self.problem_analysis.constraints_analysis_table,
        )

    def fade_in_constraint_explanation_text(self):
        return self.problem_analysis.get_constraint_explanations(1).animate.set_opacity(1)

    def fade_in_second_constraint_explanation_text(self):
        return self.problem_analysis.get_constraint_explanations(2).animate.set_opacity(1)

    def fade_out_table_for_constraint_three_explanation(self):
        return FadeOut(
            self.problem_analysis.title_tex,
            self.problem_analysis.constraints_analysis_table,
            self.problem_analysis.get_constraint_explanations(1),
            self.problem_analysis.get_constraint_explanations(2),
        )

    def fade_in_constraints_table_for_four(self):
        return FadeIn(
            self.problem_analysis.title_tex,
            self.problem_analysis.constraints_analysis_table,
        )

    def fade_in_third_constraint_explanation(self):
        return self.problem_analysis.get_constraint_explanations(3).animate.set_opacity(1)

    def shrink_pointer(self):
        return self.sll_for_normal_removal.shrink_pointer(self.sll_for_normal_removal.get_node(1).next_pointer)


class TestStream:
    def __init__(
        self,
        present_problem: PresentProblem,
        special_notes_list,
        problem_analysis: ProblemAnalysis,
        scene: BaseScene,
        shared,
        **kwargs,
    ) -> None:
        self.present_problem = present_problem
        self.special_notes_list = special_notes_list
        self.problem_analysis = problem_analysis
        self.scene = scene
        self.shared = shared

    def test_statement_header(self):
        from manim import Square

        return FadeIn(Square(), run_time=15.0)

    def fade_in_new_statement(self):
        new_statement = self.present_problem._create_statement(
            "There is a singly linked list called head and a node that we wish to"
            " remove called node. You will not be given access to the head of the"
            " list. Instead, you will be given access to the node to be deleted.",
            font_size=STATEMENT_FONT_SIZE,
        )
        self.present_problem._position_element_below_other(new_statement, self.present_problem.statement_header_tex)
        return FadeIn(new_statement)

    def fade_in_constraint_setup(self):
        self.problem_analysis.title_tex.to_edge(UP)

        return FadeIn(
            self.problem_analysis.title_tex,
            self.problem_analysis.constraints_analysis_table,
        )

    def fade_out_table(self):
        return FadeOut(
            self.problem_analysis.title_tex,
            self.problem_analysis.constraints_analysis_table,
        )

    def fade_in_first_requirement_met(self):
        return self.shared.first_requirement.animate.set_opacity(1)

    def fade_in_second_requirement_met(self):
        return self.shared.second_requirement.animate.set_opacity(1)

    def fade_out_explanation(self):
        return FadeOut(*self.scene.scene_mobjects)

    def fade_in_constraint_three_explanation_title(self):
        self.constraint_two_explanation_title = ProblemText.create_title(
            "Remove the value 2 from the linked list",
        )
        self.constraint_two_explanation_title.to_edge(UP)
        self.constraint_two_sll = SinglyLinkedList(9, 2, 5, 2, 2)

        return FadeIn(
            self.constraint_two_explanation_title,
            self.constraint_two_sll,
        )

    def highlight_value_text(self):
        return Wait()
        # return Circumscribe(self.constraint_two_explanation_title.get_sub_tex("value"))

    def fade_in_question_mark(self):
        question_mark = ProblemText.create_statement("?")
        question_mark.next_to(self.constraint_two_sll, UP)
        self.shared.pointers: list[SimplePointer] = []
        num_nodes_with_value_2_seen = 0
        starts = [0.1, 0.1, 0.08]
        for node in self.constraint_two_sll:
            if not node.data_equals(2):
                continue

            question_mark_to_node_path = Line(
                start=question_mark,
                end=node.get_container_top(),
            )
            self.shared.pointers.append(
                SimplePointer(
                    start=question_mark_to_node_path.point_from_proportion(
                        starts[num_nodes_with_value_2_seen],
                    ),
                    end=question_mark_to_node_path.point_from_proportion(0.9),
                ),
            )

            num_nodes_with_value_2_seen += 1

        return FadeIn(question_mark)

    def fade_out_constraint_three_explanation(self):
        return FadeOut(*self.scene.scene_mobjects)


class ThirdStream:
    def __init__(self, shared, **kwargs) -> None:
        self.shared = shared

    def move_arrows_to_nodes(self):
        return Write(
            VGroup(
                *[arrow for arrow in self.shared.pointers],
            ),
            run_time=2.0,
        )
