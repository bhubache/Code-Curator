from __future__ import annotations

from manim import AnimationGroup
from manim import Brace
from manim import Circumscribe
from manim import config
from manim import Create
from manim import DOWN
from manim import FadeIn
from manim import FadeOut
from manim import Flash
from manim import GrowFromCenter
from manim import Indicate
from manim import LEFT
from manim import Line
from manim import ORIGIN
from manim import Rectangle
from manim import RIGHT
from manim import ShrinkToCenter
from manim import there_and_back
from manim import Transform
from manim import UP
from manim import Wait

from code_curator.base_scene import BaseScene
from code_curator.videos.interview_problems.problem_text import ProblemText
from code_curator.data_structures.singly_linked_list import SinglyLinkedList
from code_curator.animations.singly_linked_list.transform_sll import TransformSinglyLinkedList
from code_curator.code.curator_code import CuratorCode
from code_curator.code.curator_code import remove, add, edit


TITLE = "Reverse Linked List"
PROBLEM_STATEMENT = r"Given the \code{head} of a singly linked list, reverse the list, and return \textit{the reversed list}."
CONSTRAINTS = (
    r"The number of nodes in the list is in the range \code{[0, 5000]}",
    r"\code{-5000 \leqq Node.val \leqq 5000}",
)


class Video(BaseScene):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title_tex = ProblemText.create_title(TITLE)
        self.statement_header_tex = ProblemText.create_header("Statement")
        self.statement_tex = ProblemText.create_statement(PROBLEM_STATEMENT)
        self.clarifying_questions_partition = Line(
            (-10, 0, 0),
            (10, 0, 0),
            color=self.title_tex.color,
        ).move_to(ORIGIN)
        self.clarifying_questions_header = ProblemText.create_header("Clarifying Questions")
        self.clarifying_questions_hints_list = ProblemText.create_list(
            "Parts of the question that are unclear",
            "Edge cases",
        )

        self.sll = SinglyLinkedList.create_sll(10, -2, 7, 0, color=self.title_tex.color).add_null().add_head_pointer().add_tail_pointer()
        self.sll_state_list = ProblemText.create_list(
            "Head pointer",
            "Optional tail pointer",
            "Node value",
            "Number of nodes",
        )

    def fade_in_title(self):
        self.add(self.title_tex)
        self.title_tex.set_opacity(0)
        return self.title_tex.animate.set_opacity(1).to_edge(UP)

    def fade_in_statement_header(self):
        title_copy = self.title_tex.copy().to_edge(UP)
        self.statement_header_tex.next_to(title_copy, DOWN)
        self.statement_header_tex.to_edge(LEFT)
        return FadeIn(self.statement_header_tex)

    def fade_in_statement(self):
        self.statement_tex.next_to(self.statement_header_tex, DOWN)
        self.statement_tex.to_edge(LEFT)
        return FadeIn(self.statement_tex)

    def fade_in_clarifying_questions_header(self):
        self.clarifying_questions_partition.next_to(self.statement_tex, DOWN)
        self.clarifying_questions_header.align_to(self.clarifying_questions_partition, DOWN).shift(DOWN * 0.5)
        self.clarifying_questions_hints_list.next_to(self.clarifying_questions_header, DOWN).to_edge(LEFT).set_opacity(0)
        self.add(self.clarifying_questions_hints_list)
        return (
            Create(self.clarifying_questions_partition, run_time=2),
            FadeIn(self.clarifying_questions_header, run_time=2),
        )

    def fade_in_first_clarifying_questions_point(self):
        return self.clarifying_questions_hints_list[0].animate.set_opacity(1)

    def fade_in_second_clarifying_questions_point(self):
        return self.clarifying_questions_hints_list[1].animate.set_opacity(1)

    def fade_in_edge_case_header(self):
        return (
            self.clarifying_questions_hints_list[0].animate.set_opacity(0),
            self.clarifying_questions_hints_list[1].animate.move_to(self.clarifying_questions_hints_list[0]).to_edge(LEFT),
        )

    def fade_in_list_node_code(self):
        self.code = CuratorCode(
            code="\n".join(
                (
                    "class ListNode:",
                    "    def __init__(self, val=0, next_=None):",
                    "        self.val = val",
                    "        self.next = next_",
                ),
            ),
        )
        # self.code.add_highlighter(
        #     start_line=1,
        #     height_buff=0.05,
        #     width_buff=0.1,
        # )
        # self.code.move_highlighter_to_substring(
        #     substring="next",
        #     occurrence=1,
        # )
        return FadeIn(self.code)

    def highlight_first_node_attr(self):
        return self.code.animate.saturation_highlight_lines(3)

    def highlight_second_node_attr(self):
        return self.code.animate.saturation_highlight_lines(4)

    def highlight_first_node_attr_again(self):
        return self.code.animate.saturation_highlight_lines(3)

    def fade_in_first_clarifying_question(self):
        self.first_clarifying_question = ProblemText.create_tex("What is the lower and upper bound for a node's value?")
        self.first_clarifying_question.to_edge(LEFT)
        return FadeIn(self.first_clarifying_question)

    def highlight_second_node_attr_again(self):
        return self.code.animate.saturation_highlight_lines(4)

    def fade_in_second_clarifying_question(self):
        self.second_clarifying_question = ProblemText.create_tex("What is the lower and upper bound on the number of node's in the linked list?")
        self.second_clarifying_question.to_edge(LEFT)
        self.second_clarifying_question.next_to(self.first_clarifying_question, DOWN)
        return FadeIn(self.second_clarifying_question)

    def SKIP_TO_IMPLEMENTATION(self):
        ...

    def fade_to_recursive_implementation(self):
        return [FadeOut(mobject) for mobject in self.submobjects]

    def fade_in_first_step_for_recursion(self):
        self.recursive_steps = ProblemText.create_list(
            "Identify the base cases",
            "Identify the recursive cases",
        )

        self.recursive_steps[1].set_opacity(0)

        return FadeIn(self.recursive_steps)

    def fade_in_second_step_for_recursion(self):
        return self.recursive_steps[1].animate.set_opacity(1)

    def setup_cases_determination(self):
        self.base_cases_header = (
            ProblemText.create_header(
                "Base Cases",
                color=self.title_tex.color,
            ).scale(0.75).to_edge(LEFT, buff=0.1).to_edge(UP, buff=0.1)
        )
        self.recursive_cases_header = (
            ProblemText.create_header(
                "Recursive Cases",
                color=self.title_tex.color,
            ).scale(0.75).to_edge(LEFT, buff=0.1)
        )

        self.line_partitioning_cases = Line(
            (-config["frame_x_radius"], 0, 0),
            (config["frame_x_radius"], 0, 0),
            color=self.title_tex.color,
            stroke_width=1.5,
        )

        self.recursive_cases_header.align_to(self.line_partitioning_cases, UP).shift(DOWN * 0.1)

        run_time = 2
        return (
            Transform(self.recursive_steps[0], self.base_cases_header, run_time=run_time),
            Transform(self.recursive_steps[1], self.recursive_cases_header, run_time=run_time),
            # Create(self.line_partitioning_code_and_cases, run_time=run_time),
            Create(self.line_partitioning_cases, run_time=run_time),
        )

    def fade_in_empty_linked_list(self):
        self.pondering_rectangle = Rectangle(color=self.title_tex.color, fill_color=config["background_color"], fill_opacity=1, stroke_width=1.5)
        self.empty_sll = SinglyLinkedList.create_sll(color=self.title_tex.color).add_null().add_head_pointer()

        return GrowFromCenter(self.pondering_rectangle), GrowFromCenter(self.empty_sll)

    def move_empty_sll_to_base_cases(self):
        return self.empty_sll.animate.move_to(
            (
                (-config["frame_x_radius"]) / 2,
                config["frame_y_radius"] / 2,
                0,
            ),
        )

    def fade_in_algorithm_build_up(self):
        self.line_partitioning_code_and_cases = Line(
            (0, 10, 0),
            (0, -10, 0),
        ).to_edge(RIGHT, buff=0).match_style(self.line_partitioning_cases).set_opacity(0)
        self.add(self.line_partitioning_code_and_cases)

        # Make sure pondering rectangle stays on top of the line partitioning the code from the cases
        self.add(self.pondering_rectangle)

        return (
            self.line_partitioning_code_and_cases.animate.move_to(ORIGIN).set_opacity(1),
            self.line_partitioning_cases.animate.put_start_and_end_on(
                self.line_partitioning_cases.get_start(),
                ORIGIN,
            )
        )

    def fade_in_first_base_case_code(self):
        self.first_recursive_solution_code = CuratorCode(
            code="\n".join(
                (
                    "class Solution:",
                    "    def reverseList(self, head):",
                    "        if head is None:",
                    "            return head",
                ),
            ),
        ).move_to((config["frame_x_radius"] / 2, 0, 0))

        return FadeIn(self.first_recursive_solution_code)

    def fade_in_one_node_linked_list(self):
        self.one_node_sll = SinglyLinkedList.create_sll(0, color=self.title_tex.color).add_null().add_head_pointer()
        return GrowFromCenter(self.one_node_sll)

    def indicate_empty_linked_list_as_subproblem(self):
        return Circumscribe(self.one_node_sll.null, run_time=2, stroke_width=2)

    def move_one_node_sll_to_base_cases(self):
        return self.empty_sll.animate.move_to(
            (
                (-config["frame_x_radius"] + self.empty_sll.get_center()[0]) / 2,
                self.empty_sll.get_center()[1],
                0,
            ),
        ), self.one_node_sll.animate.move_to(
            (
                self.empty_sll.get_center()[0] / 2,
                self.empty_sll.get_center()[1],
                0,
            ),
        )

    def fade_in_second_base_case_code(self):
        return self.first_recursive_solution_code.animate(run_time=6).change_source_code(
            new_code_string="\n".join(
                (
                    "class Solution:",
                    "    def reverseList(self, head):",
                    f"        if head is None{add(' or head.next is None')}:",
                    "            return head"
                ),
            ),
            saturate_edits=True,
        )


    # def fade_in_sll(self):
    #     self.sll.shift(DOWN * 1)
    #     return FadeIn(self.sll)

    # def indicate_head_pointer(self):
    #     self.add(self.sll_state_list)
    #     self.sll_state_list.set_opacity(0)
    #     return Flash(self.sll.head_pointer), self.sll_state_list[0].animate.set_opacity(1)

    # def indicate_optional_tail_pointer(self):
    #     return Flash(self.sll.tail_pointer), self.sll_state_list[1].animate.set_opacity(1)

    # def indicate_node_values(self):
    #     return self.sll.animate(rate_func=there_and_back, run_time=2).saturation_indicate_node_values(
    #         other_opacity=0.25,
    #         indicated_opacity=1,
    #     ), self.sll_state_list[2].animate.set_opacity(1)

    # def indicate_number_of_nodes(self):
    #     self.brace = Brace(self.sll, color=self.title_tex.color, stroke_width=0.25)
    #     brace_label = ProblemText.create_tex("4 nodes")
    #     brace_label.next_to(self.brace, DOWN)
    #     return FadeIn(self.brace), FadeIn(brace_label), self.sll_state_list[3].animate.set_opacity(1)

    # def highlight_first_point(self):
    #     ...

    # def move_highlighter_to_second_point(self):
    #     ...

    # def move_highlighter_to_third_point(self):
    #     ...

    # def move_highlighter_to_fourth_point(self):
    #     ...

    # def fade_in_constraints_header(self):
    #     ...

    # def fade_in_first_constraint(self):
    #     ...

    # def fade_in_second_constraint(self):
    #     ...

    # def fade_to_recursive_approach(self):
    #     ...

    # def fade_in_first_recursive_step(self):
    #     ...

    # def fade_in_second_recursive_step(self):
    #     ...

    # def fade_in_empty_sll(self):
    #     ...

    # def fade_to_sll_with_one_node(self):
    #     ...

    # def show_one_node_list_contains_empty_list(self):
    #     ...
