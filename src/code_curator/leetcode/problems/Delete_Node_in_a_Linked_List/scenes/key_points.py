from __future__ import annotations

from collections.abc import Iterable
from collections.abc import Sequence
from pathlib import Path

from code_curator.code.custom_code import CustomCode
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
from code_curator.script_handling.components.animation_script.composite_animation_script import CompositeAnimationScript
from code_curator.animations.subanimations.wait import WaitSubanimation
from code_curator.animations.parallel_animation import ParallelAnimation

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
        # to the index that the data_structure_animation_2_pointers is in the returned list.
        # fade_in_temp_trav and 1
        sll_values = [0, 1, 2, 3, 4]
        sll = SinglyLinkedList(*sll_values)

        data_structure_animation_2_pointers = (
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
            .subsequently_wave_pointer(timing_info=self.wave_pointer_1)
            .subsequently_curve_pointer(timing_info=self.curve_pointer_1)
            .subsequently_fade_out_container(timing_info=self.fade_out_container_1)
                .with_fade_out_pointer()
            .subsequently_flatten_list(timing_info=self.flatten_list_1)
                .with_fade_out_first_temp_trav()
                .with_fade_out_second_temp_trav()
                .with_center_sll()
            .build_animation()
        )

        code = CustomCode(Path.home() / 'ManimCS' / 'Code_Curator' / 'src' / 'code_curator' / 'leetcode' / 'problems' / 'Delete_Node_in_a_Linked_List' / 'required_files' / 'two_pointer_sll_node_removal.java',
                          background='rectangle')

        code.set_opacity(0)
        self.add(code)

        sll_1_pointer = SinglyLinkedList(*sll_values)
        code_1_pointer_path = (
            Path(self.problem_dir)
            / 'required_files'
            / 'one_pointer_sll_node_removal.java'
        )
        code_1_pointer = CustomCode(
            file_name=code_1_pointer_path,
            font_size=16,
            background='rectangle',
            background_stroke_width=0.5,
            stroke_width=0.01,
            background_color='#484c52',
            style='vim',
            position_relative_to=sll_1_pointer,
            move_up=0.5,
        )
        code_1_pointer.set_opacity(0)
        self.add(code_1_pointer)

        data_structure_animation_1_pointer = (
            sll_1_pointer.remove_at(
                index=2,
                display_first_trav=True,
                fade_in_temp_trav_timing_info=self.next_fade_in_temp_trav_3,
                move_first_temp_trav_timing_info=self.next_move_first_temp_trav_n_3,
            )
            .subsequently_wave_pointer(timing_info=self.next_wave_pointer_3)
            .subsequently_shrink_pointer(timing_info=self.next_shrink_pointer_3)
            .subsequently_unshrink_pointer(timing_info=self.next_unshrink_pointer_3)
            .subsequently_curve_pointer(timing_info=self.next_curve_pointer_3)
            .subsequently_fade_out_container(timing_info=self.next_fade_out_container_3)
                .with_fade_out_pointer()
            .subsequently_flatten_list(timing_info=self.next_flatten_list_3)
                .with_fade_out_first_temp_trav()
                .with_center_sll()
            .build_animation()
        )

        return [
            FadeIn(sll),
            AnimationGroup(
                ParallelAnimation(
                    'Now, take p1s next pointer and',
                    'set it equal',
                    'to p2.',
                    'We have now effectively removed the node from the linked list.',
                    # 'We have now effectively',
                    time_keepers=(
                        self.wave_pointer_1,
                        self.curve_pointer_1,
                        self.fade_out_container_1,
                    ),
                    animations=[
                        code.get_opacity_animation('p1.next'),
                        code.get_opacity_animation('='),
                        code.get_opacity_animation('p2;'),
                        code.get_fade_out_animation(),
                    ],
                ).build(),
                data_structure_animation_2_pointers,
            ),
            AnimationGroup(
                FadeOut(sll),
                FadeIn(sll_1_pointer),
            ),
            AnimationGroup(
                ParallelAnimation(
                    'the list and is not',
                    "a tail node ok now that we've been introduced",
                    "to the problem let's try to understand",
                    'the problem constraints because they can',
                    'often provide insight about the solution',
                    'at first glance the first constraint may seem',
                    # 'quite strange why is the lower bound 2 is',
                    time_keepers=(
                        self.next_fade_in_temp_trav_3,
                        self.next_move_first_temp_trav_n_3,
                        self.next_wave_pointer_3,
                        self.next_shrink_pointer_3,
                        self.next_unshrink_pointer_3,
                        self.next_curve_pointer_3,
                        self.next_fade_out_container_3,
                        # self.next_flatten_list_1,
                    ),
                    animations=[
                        code_1_pointer.get_opacity_animation('p1.next'),
                        code_1_pointer.get_opacity_animation('='),
                        code_1_pointer.get_opacity_animation('p1', occurrence=2),
                        code_1_pointer.get_opacity_animation('.next', occurrence=2),
                        code_1_pointer.get_opacity_animation('.next;'),
                        code_1_pointer.get_fade_out_animation(),
                    ],
                ).build(),
                data_structure_animation_1_pointer,
            ),
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
