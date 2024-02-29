from __future__ import annotations

import itertools as it

from manim import AnimationGroup
from manim import BLACK
from manim import Brace
from manim import Circumscribe
from manim import config
from manim import Create
from manim import DOWN
from manim import FadeIn
from manim import FadeOut
from manim import Flash
from manim import GRAY
from manim import GrowFromCenter
from manim import Indicate
from manim import LEFT
from manim import Line
from manim import ORIGIN
from manim import Rectangle
from manim import RIGHT
from manim import ShrinkToCenter
from manim import there_and_back
from manim import Text
from manim import Transform
from manim import UP
from manim import VGroup
from manim import Wait

from code_curator.base_scene import BaseScene
from code_curator.videos.interview_problems.problem_text import ProblemText
from code_curator.data_structures.singly_linked_list import SinglyLinkedList
from code_curator.data_structures.stack import Stack
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
        self.horizontal_line = Line(
            (-config["frame_x_radius"], 0, 0),
            (config["frame_x_radius"], 0, 0),
            color=self.title_tex.color,
            stroke_width=1.5,
        )
        
        self.vertical_line = Line(
            (0, 0, 0),
            (0, -config["frame_y_radius"], 0),
        ).match_style(self.horizontal_line)

        self.base_cases_header = (
            ProblemText.create_header(
                "Base Cases",
                color=self.title_tex.color,
            ).scale(0.75).to_edge(LEFT, buff=0.1)
        ).align_to(self.horizontal_line, UP).shift(DOWN * 0.1)

        self.recursive_cases_header = (
            ProblemText.create_header(
                "Recursive Cases",
                color=self.title_tex.color,
            ).scale(0.75).next_to(self.vertical_line, buff=0.1)
        ).align_to(self.horizontal_line, UP).shift(DOWN * 0.1)

        self.pondering_rectangle = Rectangle(
            width=self.horizontal_line.get_length(),
            height=self.vertical_line.get_length(),
        ).to_edge(UP, buff=0).to_edge(LEFT, buff=0)
        self.base_cases_rectangle = Rectangle(
            width=self.horizontal_line.get_length() / 2,
            height=self.vertical_line.get_length(),
        ).to_edge(DOWN, buff=0).to_edge(LEFT, buff=0)
        self.recursive_cases_rectangle = self.base_cases_rectangle.copy().to_edge(RIGHT, buff=0)

        run_time = 2
        return (
            Transform(self.recursive_steps[0], self.base_cases_header, run_time=run_time),
            Transform(self.recursive_steps[1], self.recursive_cases_header, run_time=run_time),
            Create(self.horizontal_line, run_time=run_time),
            Create(self.vertical_line, run_time=run_time),
        )

    def fade_in_empty_linked_list(self):
        self.empty_sll = SinglyLinkedList.create_sll(color=self.title_tex.color).add_null().add_head_pointer().move_to(self.pondering_rectangle.get_center())

        return FadeIn(self.empty_sll)

    def move_empty_sll_to_base_cases(self):
        return self.empty_sll.animate.move_to(
            self.base_cases_rectangle,
        )

    def fade_in_algorithm_build_up(self):
        self.pondering_rectangle = self.base_cases_rectangle.copy().to_edge(UP, buff=0).to_edge(LEFT, buff=0)
        self.code_rectangle = self.pondering_rectangle.copy().to_edge(RIGHT, buff=0)

        self.first_recursive_solution_code = CuratorCode(
            code="\n".join(
                (
                    "class Solution:",
                    "    def reverseList(self, head):",
                ),
            ),
        ).move_to(self.code_rectangle)

        return self.vertical_line.animate.put_start_and_end_on(
            (0, config["frame_y_radius"], 0),
            self.vertical_line.get_end(),
        ), FadeIn(self.first_recursive_solution_code)

    def fade_in_first_base_case_code(self):
        new_code_string = "\n".join(
            (
                "class Solution:",
                "    def reverseList(self, head):",
                add("        if head is None:"),
                add("            return head"),
            ),
        )
        return self.first_recursive_solution_code.animate.change_source_code(
            new_code_string=new_code_string,
            saturate_edits=False,
        )

    def fade_in_one_node_linked_list(self):
        self.one_node_sll = SinglyLinkedList.create_sll(0, color=self.title_tex.color).add_null().add_head_pointer().move_to(self.pondering_rectangle)
        return FadeIn(self.one_node_sll)

    def indicate_empty_linked_list_as_subproblem(self):
        return Circumscribe(self.one_node_sll.null, run_time=2, stroke_width=2)

    def move_one_node_sll_to_base_cases(self):
        return self.empty_sll.animate.move_to(
            (
                (-self.base_cases_rectangle.width * 2) / 3,
                self.empty_sll.get_center()[1],
                0,
            ),
        ), self.one_node_sll.animate.move_to(
            (
                -self.base_cases_rectangle.width / 3,
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
                    "            return head",
                ),
            ),
            saturate_edits=True,
        )

    def fade_in_two_node_linked_list(self):
        self.two_node_sll = SinglyLinkedList.create_sll(0, 1, color=self.title_tex.color).add_null().move_to(self.pondering_rectangle)
        self.two_node_sll.add_labeled_pointer(self.two_node_sll.head, "head", direction=DOWN, center=False)
        return FadeIn(self.two_node_sll)

    def fade_in_recursive_call(self):
        newline = "\n"
        new_code_string="\n".join(
            (
                "class Solution:",
                "    def reverseList(self, head):",
                "        if head is None or head.next is None:",
                f"            return head{add(newline)}",
                add("        reverseList(head.next)"),
            ),
        )
        return self.first_recursive_solution_code.animate.change_source_code(
            new_code_string=new_code_string,
            saturate_edits=False,
        )

    def prepare_for_recursive_example_step_through(self):
        # Implement some nice transition
        # TODO CUR-27: Fix adding highlighter via animation (it adds two to the screen)
        self.shift_off_screen_vgroup = VGroup(
            self.base_cases_header,
            self.recursive_cases_header,
            self.recursive_steps[0],
            self.recursive_steps[1],
            self.empty_sll,
            self.one_node_sll,
            self.horizontal_line,
        )

        self.first_recursive_solution_code.add_highlighter(start_line=2)

        run_time = 2

        return (
            self.shift_off_screen_vgroup.animate(run_time=run_time).shift(DOWN * (self.horizontal_line.get_length() / 2)),
            self.two_node_sll.animate(run_time=run_time).align_to(ORIGIN, DOWN),
            self.first_recursive_solution_code.animate(run_time=run_time).align_to(ORIGIN, DOWN),
        )

    def add_call_stack(self):
        self.call_stack = Stack(
            width=2,
            height=3,
            color=GRAY,
        )

        self.call_stack.move_to(self.base_cases_rectangle)

        return (
            FadeIn(self.call_stack),
            self.two_node_sll.animate.move_to(self.pondering_rectangle),
        )

    def push_initial_call_on_to_call_stack(self):
        return self.call_stack.animate.push("reverseList(0)")

    def first_base_case(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_substring("head is None")

    def second_base_case(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_substring("head.next is None")

    def move_highlighter_to_recursive_call(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_line(6)

    def make_first_recursive_call(self):
        return (
            self.first_recursive_solution_code.animate.move_highlighter_to_line(2),
            self.call_stack.animate.push("reverseList(1)"),
            self.two_node_sll.animate.move_labeled_pointer("head", self.two_node_sll.get_next(self.two_node_sll.head)),
        )

    def first_base_case_again(self):
        return self.first_base_case()

    def second_base_case_again(self):
        return self.second_base_case()

    def enter_if_block(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_line(4)

    def pop_off_call_stack(self):
        return (
            self.call_stack.animate.pop(),
            self.first_recursive_solution_code.animate.move_highlighter_to_line(6),
            self.two_node_sll.animate.move_labeled_pointer("head", self.two_node_sll.head),
        )

    def pop_off_call_stack_last_time(self):
        return self.call_stack.animate.pop()

    def add_print_statements(self):
        new_code_string="\n".join(
            (
                "class Solution:",
                "    def reverseList(self, head):",
                "        if head is None or head.next is None:",
                "            return head",
                "",
                add('        print("before: {head.val}")'),
                "        reverseList(head.next)",
                add('        print("after: {head.val}")'),
            ),
        )

        return self.first_recursive_solution_code.animate.change_source_code(
            new_code_string=new_code_string,
            saturate_edits=False,
        )

    def setup_print_statement_step_through(self):
        self.four_node_linked_list = (
            SinglyLinkedList.create_sll(0, 1, 2, 3, color=self.title_tex.color)
            .add_null()
        )
        self.four_node_linked_list.add_labeled_pointer(self.four_node_linked_list.head, label="head").move_to(self.pondering_rectangle)
        self.terminal = self.recursive_cases_rectangle.copy().set_stroke_width(0).set_fill(color="#1C1C1C").set_fill(color=BLACK)
        font = "MesloLGS Nerd Font Mono"
        self.printed_lines = [
            Text("before: 0", font=font),
            Text("before: 1", font=font),
            Text("before: 2", font=font),
            Text("after: 2", font=font),
            Text("after: 1", font=font),
            Text("after: 0", font=font),
        ]

        self.printed_lines[0].align_to(self.recursive_cases_rectangle, UP + LEFT)
        for prev, next_ in it.pairwise(self.printed_lines):
            self.add(prev)
            self.add(next_)
            prev.set_opacity(0)
            next_.set_opacity(0)

            next_.next_to(prev, DOWN)
            next_.align_to(prev, LEFT)

        self.first_recursive_solution_code.remove(self.first_recursive_solution_code.highlighter)
        
        return (
            FadeOut(self.two_node_sll),
            self.first_recursive_solution_code.animate.move_to(self.code_rectangle),
            FadeIn(self.four_node_linked_list),
            FadeIn(self.terminal),
        )

    def print_example_make_initial_call(self):
        return (
            self.call_stack.animate.push("reverseList(0)"),
            self.first_recursive_solution_code.animate.add_highlighter(2),
        )

    def print_example_initial_call_fail_first_base_case(self):
        return self.first_base_case()

    def print_example_initial_call_fail_second_base_case(self):
        return self.second_base_case()

    def print_example_initial_call_skip_if_block(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_line(6)

    def print_example_initial_call_print_before(self):
        return self.printed_lines[0].animate.set_opacity(1)

    def print_example_initial_call_move_to_recursive_call_line(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_line(7)

    def print_example_make_first_recursive_call(self):
        return (
            self.first_recursive_solution_code.animate.move_highlighter_to_line(2),
            self.call_stack.animate.push("reverseList(1)"),
            self.four_node_linked_list.animate.move_labeled_pointer("head", self.four_node_linked_list.get_next(self.four_node_linked_list.head)),
        )

    def print_example_first_recursive_call_fail_base_cases(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_line(3)

    def print_example_first_recursive_call_skip_if_block(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_line(6)

    def print_example_first_recursive_call_before_print(self):
        return self.printed_lines[1].animate.set_opacity(1)

    def print_example_first_recursive_call_move_to_recursive_call_line(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_line(7)

    def print_example_make_second_recursive_call(self):
        return (
            self.first_recursive_solution_code.animate.move_highlighter_to_line(2),
            self.call_stack.animate.push("reverseList(2)"),
            self.four_node_linked_list.animate.move_labeled_pointer(
                "head",
                self.four_node_linked_list.get_next(
                    self.four_node_linked_list.get_next(
                        self.four_node_linked_list.head,
                    ),
                ),
            ),
        )

    def print_example_second_recursive_call_fail_base_cases(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_line(3)

    def print_example_second_recursive_call_skip_if_block(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_line(6)

    def print_example_second_recursive_call_before_print(self):
        return self.printed_lines[2].animate.set_opacity(1)

    def print_example_second_recursive_call_move_to_recursive_call_line(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_line(7)

    def print_example_make_third_recursive_call(self):
        return (
            self.first_recursive_solution_code.animate.move_highlighter_to_line(2),
            self.call_stack.animate.push("reverseList(3)"),
            self.four_node_linked_list.animate.move_labeled_pointer(
                "head",
                self.four_node_linked_list.get_next(
                    self.four_node_linked_list.get_next(
                        self.four_node_linked_list.get_next(
                            self.four_node_linked_list.head,
                        ),
                    ),
                ),
            ),
        )

    def print_example_third_recursive_call_pass_base_cases(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_line(3)

    def print_example_third_recursive_call_enter_if_block(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_line(4)

    def print_example_pop_third_recursive_call(self):
        return (
            self.first_recursive_solution_code.animate.move_highlighter_to_line(7),
            self.call_stack.animate.pop(),
            self.four_node_linked_list.animate.move_labeled_pointer(
                "head",
                self.four_node_linked_list.get_next(
                    self.four_node_linked_list.get_next(
                        self.four_node_linked_list.head,
                    ),
                ),
            ),
        )

    def print_example_second_recursive_call_move_to_last_print(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_line(8)

    def print_example_second_recursive_call_last_print(self):
        return self.printed_lines[3].animate.set_opacity(1)

    def print_example_pop_second_recursive_call(self):
        return (
            self.first_recursive_solution_code.animate.move_highlighter_to_line(7),
            self.call_stack.animate.pop(),
            self.four_node_linked_list.animate.move_labeled_pointer(
                "head",
                self.four_node_linked_list.get_next(
                    self.four_node_linked_list.head,
                ),
            ),
        )

    def print_example_first_recursive_call_move_to_last_print(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_line(8)

    def print_example_first_recursive_call_last_print(self):
        return self.printed_lines[4].animate.set_opacity(1)

    def print_example_pop_first_recursive_call(self):
        return (
            self.first_recursive_solution_code.animate.move_highlighter_to_line(7),
            self.call_stack.animate.pop(),
            self.four_node_linked_list.animate.move_labeled_pointer(
                "head",
                self.four_node_linked_list.head,
            ),
        )

    def print_example_initial_call_move_to_last_print(self):
        return self.first_recursive_solution_code.animate.move_highlighter_to_line(8)

    def print_example_initial_call_last_print(self):
        return self.printed_lines[5].animate.set_opacity(1)

    def print_example_pop_initial_call(self):
        return (
            # self.first_recursive_solution_code.animate.move_highlighter_to_line(7),
            self.call_stack.animate.pop(),
            # self.four_node_linked_list.animate.move_labeled_pointer(
            #     "head",
            #     self.four_node_linked_list.get_next(
            #         self.four_node_linked_list.head,
            #     ),
            # ),
        )


