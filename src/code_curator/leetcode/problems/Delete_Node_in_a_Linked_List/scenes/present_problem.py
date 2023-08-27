"""Animations for presenting the problem."""
from __future__ import annotations

from collections.abc import Sequence
from functools import wraps
from typing import TYPE_CHECKING

from manim import Animation
from manim import AnimationGroup
from manim import FadeIn
from manim import FadeOut
from manim import Wait

from code_curator.animations.animation_generator import AnimationGenerator
from code_curator.animations.change_color import ChangeColor
from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.leetcode.problem_text import ProblemText
from code_curator.leetcode.scenes.present_problem.base_present_problem import (
    BasePresentProblem,
)


logger = CustomLogger.getLogger(__name__)


if TYPE_CHECKING:
    from manim import Tex


TITLE = "Delete Node in a Linked List"
STATEMENT = (
    r"There is a singly linked list head and we want to delete a node node in it. You"
    r" are given the node to be deleted node. You will not be given access to the first"
    r" node of head. All the values of the linked list are unique, and it is guaranteed"
    r" that the given node node is not the last node in the linked list. Delete the"
    r" given node. Note that by deleting the node, we do not mean removing it from"
    r" memory. We mean:"
)
SPECIAL_NOTES = []
SPECIAL_NOTES.append("The value of the given node should not exist in the linked list.")
SPECIAL_NOTES.append("The number of nodes in the linked list should decrease by one.")
SPECIAL_NOTES.append("All the values before node should be in the same order.")
SPECIAL_NOTES.append("All the values after node should be in the same order.")

CONSTRAINTS = []
CONSTRAINTS.append("The number of nodes in the given list is in the range [2, 1000].")
CONSTRAINTS.append(r"-1000 $\leq$ Node.val $\leq$ 1000")
CONSTRAINTS.append("The value of each node in the list is unique.")
CONSTRAINTS.append("The node to be deleted is in the list and is not a tail node.")

REMOVE_COLOR = "#FF0000"
KEEP_COLOR = "#00FF00"
RESET_COLOR = "#DBC9B8"

CustomAnimations = Sequence[Animation]


def position_special_notes_list(fn):
    @wraps(fn)
    def inner(self, *args, **kwargs):
        self._position_element_below_lowest_in_scene(self._special_notes_list)
        yield from fn(self, *args, **kwargs)

    return inner


class PresentProblem(BasePresentProblem):
    def __init__(self, problem_dir: str, aligned_animation_scene):
        super().__init__(
            title=TITLE,
            statement_header="Statement",
            statement=STATEMENT,
            constraints_header="Constraints",
            constraints=CONSTRAINTS,
            problem_dir=problem_dir,
            aligned_animation_scene=aligned_animation_scene,
            owner=None,
        )
        self._special_notes_list = ProblemText.create_constraints_list(
            SPECIAL_NOTES,
            font_size=20,
        )

    @position_special_notes_list
    def deleting_point_1(self) -> CustomAnimations:
        yield FadeIn(self._special_notes_list[0])

    def deleting_point_2(self) -> CustomAnimations:
        yield FadeIn(self._special_notes_list[1])

    def deleting_point_3(self) -> CustomAnimations:
        yield FadeIn(self._special_notes_list[2])

    def deleting_point_4(self) -> CustomAnimations:
        yield FadeIn(self._special_notes_list[3])

    def special_note(self) -> CustomAnimations:
        yield Wait()

    class remove_duplication(AnimationGenerator):
        def initialize(self) -> None:
            text_to_remove: str = (
                " All the values of the linked list are unique, and it is"
                " guaranteed that the given node node is not the last node in the"
                " linked list."
            )
            self._problem_text_to_remove: ProblemText = self._statement.get_sub_tex(
                text_to_remove,
            )
            self.second_mention_tex = self._statement.get_sub_tex(
                "Delete the given node.",
            )

        class constraints_duplication(AnimationGenerator):
            def initialize(self) -> None:
                self._third_constraint_tex: Tex = self.get_constraint_tex(3)
                self._fourth_constraint_tex: Tex = self.get_constraint_tex(4)

            def highlight_duplication(self):
                yield AnimationGroup(
                    ChangeColor(self._third_constraint_tex, KEEP_COLOR),
                    ChangeColor(self._fourth_constraint_tex, KEEP_COLOR),
                    ChangeColor(
                        self._problem_text_to_remove,
                        REMOVE_COLOR,
                        starting_color=self._statement.color,
                    ),
                )

            def remove(self):
                yield AnimationGroup(
                    FadeOut(self._problem_text_to_remove),
                    ChangeColor(self._third_constraint_tex, RESET_COLOR),
                    ChangeColor(self._fourth_constraint_tex, RESET_COLOR),
                )

        class delete_node(AnimationGenerator):
            def initialize(self) -> None:
                self.first_mention_tex = self._statement.get_sub_tex(
                    "delete a node node in it.",
                )

            def change_color(self):
                yield AnimationGroup(
                    ChangeColor(
                        self.first_mention_tex,
                        KEEP_COLOR,
                        starting_color=self._statement.color,
                    ),
                    ChangeColor(
                        self.second_mention_tex,
                        REMOVE_COLOR,
                        starting_color=self._statement.color,
                    ),
                )

            def remove(self):
                yield AnimationGroup(
                    FadeOut(self.second_mention_tex),
                    ChangeColor(self.first_mention_tex, RESET_COLOR),
                )

        def smooth_over_wording(self):
            # base = self._statement
            self._problem_text_to_remove.set_opacity(0)
            self.second_mention_tex.set_opacity(0)
            new_statement = self._create_statement(
                "There is a singly linked list called head and a node that we wish to"
                " remove called node. You will not be given access to the head of the"
                " list. Instead, you will be given access to the node to be deleted.",
            )
            self._position_element_below_other(new_statement, self._statement_header)
            yield AnimationGroup(
                FadeOut(self._statement),
                FadeIn(new_statement),
            )
            # self.add(new_statement)

            # target = new_statement
            # line = Line(2*UP, 2*DOWN, color=RED).next_to(base, LEFT, buff=1)
            # base_background = Square(
            #     fill_color=PINK,
            #     fill_opacity=0.3
            # ).rotate(PI / 2).scale(5).next_to(line, RIGHT, buff=0)
            # target_background = Square(fill_color=MAROON, fill_opacity=0.3).rotate(PI / 2).scale(5).next_to(line, LEFT, buff=0)
            # slider = VGroup(base_background, target_background, line)

            # self.add(slider)

            # def get_intersection_updater(no_added_mob, background):
            #     def updater(added_mob):
            #         grp = []
            #         extract_all_submobjects(grp, no_added_mob)
            #         added_mob.become(
            #             VGroup(
            #                 *[
            #                     Intersection(submob, background).match_style(submob)
            #                     for submob in grp
            #                 ]
            #             )
            #         )

            #     def extract_all_submobjects(grp, mob):
            #         if len(mob.submobjects) == 0:
            #             grp.append(mob)
            #         else:
            #             for submob in mob.submobjects:
            #                 extract_all_submobjects(grp, submob)
            #         # added_mob.become(Intersection(no_added_mob, background).match_style(no_added_mob))
            #     return updater

            # pre_mob = VMobject().add_updater(get_intersection_updater(base, base_background))
            # pos_mob = VMobject().add_updater(get_intersection_updater(target, target_background))
            # self.add(pre_mob, pos_mob)

            # yield slider.animate.shift(RIGHT * 4)
            # # yield FadeIn(Tex('HELLO WORLD!'))

    def _create_statement(self, text: str, font_size=25):
        return super()._create_statement(text, font_size=font_size)

    def _create_constraints(self, text: str, font_size=20):
        return super()._create_constraints(text, font_size=font_size)
