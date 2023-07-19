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
from manim import Circle
from manim import Square
from manim import Rectangle
from manim import RED
from manim import Transform
from manim import FadeOut
from manim import Tex
from code_curator.script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript

from animations.subanimations.wait import WaitSubanimation
from animations.parallel_animation import ParallelAnimation


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
        # NOTE:
        # The timing_info attributes are somewhat magical. The portions correspond to
        # the subsection in the animation_script.yaml and the integer at the end corresponds
        # to the index that the data_structure_animation is in the returned list.
        # fade_in_temp_trav and 1
        sll = SinglyLinkedList(0, 1, 2, 3, 4)
        data_structure_animation = (
            sll.remove_at(
                index=2,
                display_first_trav=True,
                display_second_trav=True,
                fade_in_temp_trav_timing_info=self.fade_in_temp_trav_1,
                move_first_temp_trav_timing_info=self.move_first_temp_trav_n_1,
                move_second_temp_trav_timing_info=self.move_second_temp_trav_n_1,
            )
            # .subsequently_shrink_pointer()
            # .subsequently_unshrink_pointer()
            # .subsequently_curve_pointer()
            .subsequently_wave_pointer(timing_info=self.wave_pointer_1)
            .subsequently_curve_pointer(timing_info=self.curve_pointer_1)
            .subsequently_fade_out_container(timing_info=self.fade_out_container_1)
                .with_fade_out_pointer()
            .subsequently_flatten_list(timing_info=self.flatten_list_1)
                .with_fade_out_first_temp_trav()
                .with_fade_out_second_temp_trav()
                .with_center_sll()
            .build_animation()

            # sll.add_last(
            #     data=1,
            # )
            # .with_fade_in_container()
            # .with_fade_in_pointer()
            # .with_move_tail()
            # .with_center_sll()
            # .build_animation(),
        )
        # data_structure_animation.insert_subanimation(-1, WaitSubanimation(3))

        # TODO: Replace FadeIn(Circle) with code animation aligned with audio
        # 1. Find lag_ratio for AnimationGroup for when code animation should start
        # 2. Determine how long code animation should last
        c = Circle()
        s = Square()
        r = Rectangle()
        return [
            FadeIn(sll),
            AnimationGroup(
                ParallelAnimation(
                    'take p1s next pointer and',
                    'set it equal',
                    'to p2.',
                    'We have',
                    time_keepers=(
                        self.wave_pointer_1,
                        self.curve_pointer_1,
                        self.fade_out_container_1,
                    ),
                    animations=[
                        FadeIn(c),
                        FadeIn(s),
                        FadeIn(r),
                        # FadeIn(Tex('hi')),
                        FadeOut(c, s, r),
                    ],
                ).build(),
                data_structure_animation,
            ),
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
