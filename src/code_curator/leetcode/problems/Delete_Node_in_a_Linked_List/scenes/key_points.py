from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Sequence

from code_curator.data_structures.pointers.simple_pointer import SimplePointer
from code_curator.data_structures.singly_linked_list import SinglyLinkedList
from code_curator.leetcode.problem_text import ProblemText
from code_curator.leetcode.scenes.key_points.base_key_points import BaseKeyPoints
from manim import Animation
from manim import AnimationGroup
from manim import FadeIn
from manim import Line
from manim import UP
from manim import Wait
from manim import Write
from code_curator.script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript


POINTS: list[str] = [
    'The node to be deleted is not the tail',
    # 'We\'re just given the node to be deleted',
]

INSIGHTS: list[str] = [
    'The node immediately after the node to be deleted is necessary',
    # 'Nodes after the node to be deleted are necessary',
]


class KeyPoints(BaseKeyPoints):
    def __init__(
        self,
        problem_dir: str,
        aligned_animation_scene: CompositeAnimationScript,
    ) -> None:
        super().__init__(
            points=POINTS, insights=INSIGHTS, problem_dir=problem_dir,
            aligned_animation_scene=aligned_animation_scene,
        )
        self.add_overriding_animation(self.key_point_1)

    def key_point_1(self) -> Iterable[Animation]:
        sll = SinglyLinkedList(0, 1, 2, 3, 4)

        return [
            FadeIn(sll),
            sll.remove_at(
                index=2,
                display_first_trav=True,
                display_second_trav=True,
            )
            .subsequently_shrink_pointer()
            .subsequently_unshrink_pointer()
            .subsequently_curve_pointer()
            .subsequently_fade_out_container()
                .with_fade_out_pointer()
            .subsequently_flatten_list()
                .with_fade_out_first_temp_trav()
                .with_fade_out_second_temp_trav()
                .with_center_sll()
            .build_animation(),
            # sll.add_last(
            #     data=1,
            # )
            # .with_fade_in_container()
            # .with_fade_in_pointer()
            # .with_move_tail()
            # .with_center_sll()
            # .build_animation(),
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
