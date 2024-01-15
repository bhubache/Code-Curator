from __future__ import annotations

from manim import AnimationGroup
from manim import Brace
from manim import Create
from manim import DOWN
from manim import FadeIn
from manim import FadeOut
from manim import Flash
from manim import Indicate
from manim import LEFT
from manim import Line
from manim import ORIGIN
from manim import there_and_back
from manim import UP
from manim import Wait

from code_curator.base_scene import BaseScene
from code_curator.leetcode.problem_text import ProblemText
from code_curator.data_structures.singly_linked_list_v2 import SinglyLinkedList
from code_curator.animations.singly_linked_list.transform_sll import TransformSinglyLinkedList


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

    def fade_in_sll(self):
        self.sll.shift(DOWN * 1)
        return FadeIn(self.sll)

    def indicate_head_pointer(self):
        self.add(self.sll_state_list)
        self.sll_state_list.set_opacity(0)
        return Flash(self.sll.head_pointer), self.sll_state_list[0].animate.set_opacity(1)

    def indicate_optional_tail_pointer(self):
        return Flash(self.sll.tail_pointer), self.sll_state_list[1].animate.set_opacity(1)

    def indicate_node_values(self):
        return self.sll.animate(rate_func=there_and_back, run_time=2).saturation_indicate_node_values(
            other_opacity=0.25,
            indicated_opacity=1,
        ), self.sll_state_list[2].animate.set_opacity(1)

    def indicate_number_of_nodes(self):
        self.brace = Brace(self.sll, color=self.title_tex.color, stroke_width=0.25)
        brace_label = ProblemText.create_tex("4 nodes")
        brace_label.next_to(self.brace, DOWN)
        return FadeIn(self.brace), FadeIn(brace_label), self.sll_state_list[3].animate.set_opacity(1)

    def highlight_first_point(self):
        ...

    def move_highlighter_to_second_point(self):
        ...

    def move_highlighter_to_third_point(self):
        ...

    def move_highlighter_to_fourth_point(self):
        ...

    def fade_in_constraints_header(self):
        ...

    def fade_in_first_constraint(self):
        ...

    def fade_in_second_constraint(self):
        ...

    def fade_to_recursive_approach(self):
        ...

    def fade_in_first_recursive_step(self):
        ...

    def fade_in_second_recursive_step(self):
        ...

    def fade_in_empty_sll(self):
        ...

    def fade_to_sll_with_one_node(self):
        ...

    def show_one_node_list_contains_empty_list(self):
        ...
