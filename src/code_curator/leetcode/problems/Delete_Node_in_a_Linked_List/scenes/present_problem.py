from __future__ import annotations

from collections.abc import Sequence
from functools import wraps
from typing import TYPE_CHECKING

import manim
from manim import Animation
from manim import AnimationGroup
from manim import FadeIn
from manim import FadeOut
from manim import Wait

from code_curator.animations.fixed_succession import FixedSuccession
from code_curator.animations.change_color import ChangeColor
from code_curator.leetcode.problem_text import ProblemText
from code_curator.leetcode.scenes.present_problem.base_present_problem import BasePresentProblem


if TYPE_CHECKING:
    from manim import Tex


TITLE = 'Delete Node in a Linked List'
STATEMENT = (
    r'There is a singly linked list head and we want to delete a node node in it. You are given the node to be deleted node. You will not be given access to the first node of head. All the values of the linked list are unique, and it is guaranteed that the given node node is not the last node in the linked list. Delete the given node. Note that by deleting the node, we do not mean removing it from memory. We mean'
)
SPECIAL_NOTES = []
SPECIAL_NOTES.append('The value of the given node should not exist in the linked list.')
SPECIAL_NOTES.append('The number of nodes in the linked list should decrease by one.')
SPECIAL_NOTES.append('All the values before node should be in the same order.')
SPECIAL_NOTES.append('All the values after node should be in the same order.')

CONSTRAINTS = []
CONSTRAINTS.append('The number of nodes in the given list is in the range [2, 1000].')
CONSTRAINTS.append(r'-1000 $\leq$ Node.val $\leq$ 1000')
CONSTRAINTS.append('The value of each node in the list is unique.')
CONSTRAINTS.append('The node to be deleted is in the list and is not a tail node.')


CustomAnimations = Sequence[Animation]


class PresentProblem(BasePresentProblem):
    def __init__(self, problem_dir: str, aligned_animation_scene):
        super().__init__(
            title=TITLE,
            statement_header='Statement',
            statement=STATEMENT,
            constraints_header='Constraints',
            constraints=CONSTRAINTS,
            problem_dir=problem_dir,
            aligned_animation_scene=aligned_animation_scene,
        )
        self._special_notes_list = ProblemText.create_constraints_list(SPECIAL_NOTES, font_size=20)

        self.add_nonoverriding_animation(self.intro)
        self.add_nonoverriding_animation(self.deleting_point_1)
        self.add_nonoverriding_animation(self.deleting_point_2)
        self.add_nonoverriding_animation(self.deleting_point_3)
        self.add_nonoverriding_animation(self.deleting_point_4)
        self.add_nonoverriding_animation(self.special_note)
        self.add_nonoverriding_animation(self.remove_duplication)

    def _create_statement(self, text: str, font_size=25):
        return super()._create_statement(text, font_size=font_size)

    def _create_constraints(self, text: str, font_size=20):
        return super()._create_constraints(text, font_size=font_size)

    def intro(self) -> CustomAnimations:
        return [Wait()]

    def position_special_notes_list(fn):
        @wraps(fn)
        def inner(self, *args, **kwargs):
            self._position_element_below_lowest_in_scene(self._special_notes_list)
            result = fn(self, *args, **kwargs)
            return result
        return inner

    @position_special_notes_list
    def deleting_point_1(self) -> CustomAnimations:
        return [FadeIn(self._special_notes_list[0])]

    def deleting_point_2(self) -> CustomAnimations:
        return [FadeIn(self._special_notes_list[1])]

    def deleting_point_3(self) -> CustomAnimations:
        return [FadeIn(self._special_notes_list[2])]

    def deleting_point_4(self) -> CustomAnimations:
        return [FadeIn(self._special_notes_list[3])]

    def special_note(self) -> CustomAnimations:
        return [Wait()]

    def remove_duplication(self) -> CustomAnimations:
        text_to_remove: str = (
            ' All the values of the linked list are unique, and it is guaranteed that the given node node is not the last node in the linked list.'
        )

        problem_text_to_remove: ProblemText = self._statement.get_sub_tex(text_to_remove)
        third_constraint_tex: Tex = self.get_constraint_tex(3)
        fourth_constraint_tex: Tex = self.get_constraint_tex(4)

        remove_color: str = '#FF0000'
        keep_color: str = '#00FF00'
        reset_color = third_constraint_tex.color

        def constraints_duplication():

            def three():
                pass

            def four():
                pass

            def statement():
                pass

            def remove():
                pass

        def delete_node():
            pass



        # return {
        #     'constraints_duplication': {
        #         'three': ChangeColor(third_constraint_tex, keep_color),
        #         'four': ChangeColor(fourth_constraint_tex, keep_color),
        #         'statement': ChangeColor(problem_text_to_remove, remove_color),
        #         'remove': AnimationGroup(
        #             FadeOut(problem_text_to_remove),
        #             ChangeColor(third_constraint_tex, reset_color),
        #             ChangeColor(fourth_constraint_tex, reset_color),
        #         ),
        #     },
        #     'delete_node': Wait(),
        # }
        return [
            Wait(),
            FixedSuccession(
                AnimationGroup(
                    ChangeColor(problem_text_to_remove, remove_color),
                    ChangeColor(third_constraint_tex, keep_color),
                    ChangeColor(fourth_constraint_tex, keep_color),
                ),
                AnimationGroup(
                    FadeOut(problem_text_to_remove),
                    ChangeColor(third_constraint_tex, reset_color),
                    ChangeColor(fourth_constraint_tex, reset_color),
                ),
            FadeIn(manim.Circle()),
            )
        ]
