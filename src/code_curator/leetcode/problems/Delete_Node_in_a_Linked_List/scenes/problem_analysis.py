from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Sequence

from code_curator.data_structures.pointers.simple_pointer import SimplePointer
from code_curator.data_structures.singly_linked_list import SinglyLinkedList
from code_curator.leetcode.problem_text import ProblemText
from code_curator.leetcode.scenes.problem_analysis.base_problem_analysis import BaseProblemAnalysis
from manim import Animation
from manim import AnimationGroup
from manim import FadeIn
from manim import Line
from manim import UP
from manim import Wait
from manim import Write
from code_curator.script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript

from .present_problem import CONSTRAINTS

# DEV IMPORTS
from code_curator.animations.subanimations.wait import WaitSubanimation
from code_curator.animations.data_structure_animation import DataStructureAnimation

EXPLANATIONS = []
EXPLANATIONS.append('Node is in the list and is not the tail node')
EXPLANATIONS.append('Not pertinent')
EXPLANATIONS.append('Not pertinent')
EXPLANATIONS.append('It\'s impossible to delete the tail')


class ProblemAnalysis(BaseProblemAnalysis):
    def __init__(self, problem_dir: str, aligned_animation_scene: CompositeAnimationScript):
        super().__init__(
            constraints=CONSTRAINTS,
            explanations=EXPLANATIONS,
            problem_dir=problem_dir,
            aligned_animation_scene=aligned_animation_scene,
        )
        self.add_overriding_animation(self.explanation_1)
        # self.add_overriding_animation(self.explanation_3)
        # self.add_overriding_animation(self.explanation_2)

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
        # return [FadeIn(Circle()), FadeIn(Square()), FadeIn(Triangle())]

    def explanation_3(self) -> Sequence[Animation]:
        title = ProblemText.create_title(
            'Remove the value 2 from the linked list',
        )
        title.to_edge(UP)
        sll = SinglyLinkedList(9, 2, 5, 2, 2)

        question_mark = ProblemText.create_statement('?')
        question_mark.next_to(sll, UP)
        pointers: list[SimplePointer] = []
        for node in sll:
            if not node.data_equals(2):
                continue

            question_mark_to_node_path = Line(
                start=question_mark, end=node.get_container_top(),
            )
            p = SimplePointer(
                start=question_mark_to_node_path.point_from_proportion(
                    0.01,
                ), end=question_mark_to_node_path.point_from_proportion(0.9),
            )
            pointers.append(p)

        return [
            FadeIn(title),
            FadeIn(sll),
            # FadeIn(question_mark),
            AnimationGroup(
                FadeIn(question_mark),
                *[Write(arrow) for arrow in pointers],
            ),
        ]
