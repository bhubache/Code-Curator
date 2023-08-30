from __future__ import annotations

from typing import TYPE_CHECKING

from manim import Animation
from manim import AnimationGroup
from manim import Circle
from manim import FadeIn
from manim import Flash
from manim import GREEN
from manim import Circumscribe
from manim import Line
from manim import Square
from manim import UP
from manim import LEFT
from manim import Tex
from manim import TransformMatchingShapes
from manim import Wait
from manim import Write

from .present_problem import CONSTRAINTS
from code_curator.animations.animation_generator import AnimationGenerator
from code_curator.animations.subanimations.wait import WaitSubanimation
from code_curator.animations.utils.utils import overriding_animation
from code_curator.animations.utils.utils import transition_overriding_start
from code_curator.data_structures.pointers.simple_pointer import SimplePointer
from code_curator.data_structures.singly_linked_list import SinglyLinkedList
from code_curator.leetcode.problem_text import ProblemText
from code_curator.leetcode.scenes.problem_analysis.base_problem_analysis import (
    BaseProblemAnalysis,
)


if TYPE_CHECKING:
    from collections.abc import Iterable
    from collections.abc import Sequence

    from code_curator.script_handling.components.animation_script.composite_animation_script import (  # noqa: E501
        CompositeAnimationScript,
    )
    from code_curator.animations.data_structure_animation import DataStructureAnimation

EXPLANATIONS = []
EXPLANATIONS.append("Node is in the list and is not the tail node")
EXPLANATIONS.append("Not pertinent")
EXPLANATIONS.append("Not pertinent")
EXPLANATIONS.append("It's impossible to delete the tail")


class ProblemAnalysis(BaseProblemAnalysis):
    def __init__(
        self,
        problem_dir: str,
        aligned_animation_scene: CompositeAnimationScript,
    ) -> None:
        super().__init__(
            constraints=CONSTRAINTS,
            explanations=EXPLANATIONS,
            problem_dir=problem_dir,
            aligned_animation_scene=aligned_animation_scene,
        )

    class ParallelAnimation:
        def parallel_1(self):
            yield FadeIn(Circle(0.1))

        def parallel_2(self):
            yield FadeIn(Circle(0.5))

        def parallel_3(self):
            yield FadeIn(Circle(1))

    @overriding_animation
    class explain_constraint_one(AnimationGenerator):

        def initialize(self) -> None:
            self.fourth_constraint = self._get_constraint_mobject(4).copy()
            self.first_check = 'is in the list'
            self.second_check = 'is not a tail node'
            self.check_list = ProblemText.create_constraints_list([self.first_check, self.second_check])
            self.sll = SinglyLinkedList(0)

        @transition_overriding_start
        def highlight_fourth_constraint(self):
            self.check_list.to_edge(UP).to_edge(LEFT)
            yield TransformMatchingShapes(self.fourth_constraint, self.check_list)

        def at_least_one_node(self):
            in_the_list_check_mark = Tex(r'$\checkmark$').scale(0.6).set_color(GREEN)
            in_the_list_check_mark.next_to(self.check_list.get_part_by_tex(self.second_check))
            in_the_list_check_mark.align_to(self.check_list, UP)
            yield AnimationGroup(
                FadeIn(in_the_list_check_mark),
                FadeIn(self.sll),
            )

        def bars_node(self):
            yield Circumscribe(self.check_list.get_part_by_tex(self.second_check), run_time_proportion=0.4)

        def both_the_head(self):
            yield Flash(self.sll.head_pointer, run_time=0.1)

        def and_tail(self):
            yield Flash(self.sll.tail_pointer, run_time=0.1)

        def at_least_two_nodes(self):
            is_not_a_tail_node_checkmark = Tex(r'$\checkmark$').scale(0.6).set_color(GREEN)
            is_not_a_tail_node_checkmark.next_to(self.check_list.get_part_by_tex(self.second_check))
            # is_not_a_tail_node_checkmark.align_to(self.check_list, UP)
            yield AnimationGroup(
                self.sll.add_last(data=1)
                .subsequently_fade_in_container()
                .with_fade_in_pointer()
                .with_center_sll()
                .with_move_tail()
                .build_animation(),
                FadeIn(is_not_a_tail_node_checkmark),
            )

    def present_second_constraint(self):
        yield FadeIn(Circle())

    @overriding_animation
    def explain_constraint_two(self):
        yield FadeIn(Circle())

    def explanation_1(self) -> Iterable[Animation]:
        sll = SinglyLinkedList(0)

        data_structure_animation: DataStructureAnimation = (
            sll.add_last(
                data=1,
            )
            .with_fade_in_container()
            .with_fade_in_pointer()
            .with_move_tail()
            .with_center_sll()
            .build_animation()
        )
        data_structure_animation.insert_subanimation(1, WaitSubanimation(3))

        return [
            Wait(),
            FadeIn(sll),
            data_structure_animation,
        ]

    def explanation_2(self) -> Sequence[Animation]:
        pass

    def explanation_3(self) -> Sequence[Animation]:
        title = ProblemText.create_title(
            "Remove the value 2 from the linked list",
        )
        title.to_edge(UP)
        sll = SinglyLinkedList(9, 2, 5, 2, 2)

        question_mark = ProblemText.create_statement("?")
        question_mark.next_to(sll, UP)
        pointers: list[SimplePointer] = []
        for node in sll:
            if not node.data_equals(2):
                continue

            question_mark_to_node_path = Line(
                start=question_mark,
                end=node.get_container_top(),
            )
            p = SimplePointer(
                start=question_mark_to_node_path.point_from_proportion(
                    0.01,
                ),
                end=question_mark_to_node_path.point_from_proportion(0.9),
            )
            pointers.append(p)

        return [
            FadeIn(title),
            FadeIn(sll),
            AnimationGroup(
                FadeIn(question_mark),
                *[Write(arrow) for arrow in pointers],
            ),
        ]
