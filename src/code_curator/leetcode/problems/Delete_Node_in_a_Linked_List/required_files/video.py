from __future__ import annotations

from manim import AnimationGroup
from manim import Arrow
from manim import config
from manim import FadeIn
from manim import FadeOut
from manim import Circumscribe
from manim import GREEN
from manim import Group
from manim import LEFT
from manim import Line
from manim import Tex
from manim import Transform
from manim import UP
from manim import VGroup
from manim import Wait
from manim import Write

from code_curator.animations.attribute_animation import AttributeAnimation
from code_curator.animations.arrow_transport_transformation import ArrowTransportTransformation
from code_curator.base_scene import BaseScene
from code_curator.leetcode.scenes.present_problem.base_present_problem import BasePresentProblem as PresentProblem
from code_curator.leetcode.scenes.problem_analysis.base_problem_analysis import BaseProblemAnalysis as ProblemAnalysis
from code_curator.main import QUALITY
from code_curator.leetcode.problem_text import ProblemText
from code_curator.animations.change_color import ChangeColor
from code_curator.animations.utils.utils import run_time_can_be_truncated
from code_curator.data_structures.singly_linked_list import SinglyLinkedList
# from code_curator.data_structures.singly_linked_list_v2 import SinglyLinkedList
from code_curator.data_structures.graph import LabeledLine
from code_curator.data_structures.pointers.simple_pointer import SimplePointer

# TODO: Try and just have the special Mobject in curator animation be in the scene.mobjects
# TODO: Consider substrings_to_isolate when creating Tex for TransformMatchingTex


TITLE = "Delete Node in a Linked List"
STATEMENT = (
    r"There is a singly linked list head and we want to delete a node node in it. You"
    r" are given the node to be deleted node. You will not be given access to the first"
    r" node of head. All the values of the linked list are unique, and it is guaranteed"
    r" that the given node node is not the last node in the linked list. Delete the"
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

    def initialize_scene(self) -> None:
        self.present_problem = PresentProblem(
            title=TITLE,
            statement=STATEMENT,
            constraints=CONSTRAINTS,
            scene=self,
        )
        self.problem_analysis = ProblemAnalysis(
            constraints=CONSTRAINTS,
            explanations=CONSTRAINT_EXPLANATIONS,
        )
        self.present_problem.statement_tex = self.present_problem._create_statement(STATEMENT, font_size=STATEMENT_FONT_SIZE)
        self.present_problem.constraints_tex = self.present_problem._create_constraints(CONSTRAINTS, font_size=20, buff=0.20)
        self.special_notes_list = ProblemText.create_constraints_list(
            SPECIAL_NOTES,
            font_size=20,
            buff=0.20,
        )


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
            " linked list."
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
            )
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

    def fade_out_everything(self):
        mobjects_to_fade_out = self.scene.scene_mobjects
        # mobjects_to_fade_out.remove()
        return FadeOut(*mobjects_to_fade_out)

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
        self.sll.head_pointer.set_opacity(0)
        self.sll.tail_pointer.set_opacity(0)
        return FadeIn(self.sll)

    def fade_in_head(self):
        return self.sll.head_pointer.animate(run_time=0.3).set_opacity(1)

    def fade_in_tail(self):
        return self.sll.tail_pointer.animate(run_time=0.3).set_opacity(1)

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

    def fade_out_constraints_table_for_constraint_four_explanation(self):
        return FadeOut(*self.scene.scene_mobjects)

    def fade_in_linked_list(self):
        self.sll_for_normal_removal = SinglyLinkedList(0, 1, 2, 3, 4, show_null=True)
        # self.pointer_p = LabeledLine(self.sll_for_normal_removal.get_node(0), direction=UP)
        # self.pointer_p = self.sll_for_normal_removal.add_incoming_arrow_at_index(
        #     0,
        #     direction=UP,
        #     name="p",
        # )
        return FadeIn(self.sll_for_normal_removal)

    @run_time_can_be_truncated
    def advance_pointer(self):
        return Wait()
        return (
            self.sll_for_normal_removal
            .advance_pointer(self.pointer_p)
        )

    def wave_pointer(self):
        return Wait()
        return self.sll_for_normal_removal.wave_pointer(
            self.sll_for_normal_removal[1].pointer_to_next,
        )

    def shrink_pointer(self):
        return Wait()
        # return self.sll_for_normal_removal.


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
            "Remove the value 2 from the linked list"
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
                )
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
                *[
                    arrow
                    for arrow in self.shared.pointers
                ]
            ),
            run_time=2.0,
        )
