from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Sequence

from data_structures.pointers.simple_pointer import SimplePointer
from data_structures.singly_linked_list import SinglyLinkedList
from leetcode.problem_text import ProblemText
from leetcode.scenes.key_points.base_key_points import BaseKeyPoints
from manim import Animation
from manim import AnimationGroup
from manim import FadeIn
from manim import Line
from manim import UP
from manim import Wait
from manim import Write
from script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript


POINTS: list[str] = [
    'The node to be deleted is not the tail',
    'We\'re just given the node to be deleted',
]

INSIGHTS: list[str] = [
    'The node immediately after the node to be deleted is necessary',
    'Nodes after the node to be deleted are necessary',
]


class KeyPoints(BaseKeyPoints):
    def __init__(
        self,
        points: list[str],
        insights: list[str],
        problem_dir: str,
        aligned_animation_scene: CompositeAnimationScript,
    ) -> None:
        super().__init__(
            points=points, insights=insights, problem_dir=problem_dir,
            aligned_animation_scene=aligned_animation_scene,
        )

    def explanation_1(self) -> Iterable[Animation]:
        sll = SinglyLinkedList(0)

        return [
            FadeIn(sll),
            sll.add_last(
                data=1,
            )
            .with_fade_in_container()
            .with_fade_in_pointer()
            .with_move_tail()
            .with_center_sll()
            .build_animation(),
            Wait(),
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
            FadeIn(question_mark),
            AnimationGroup(
                *[Write(arrow) for arrow in pointers],
            ),
        ]
