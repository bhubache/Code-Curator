'''
TODO
- Allow person to put in basic text and have parser convert it to something that's readable by Tex
'''
from __future__ import annotations

from collections.abc import Callable

from base_scene import BaseScene
from custom_logging.custom_logger import CustomLogger
from leetcode.problem_text import ProblemText
from manim import Animation
from manim import DOWN
from manim import FadeIn
from manim import LEFT
from manim import UP
from manim import Wait
from script_handling.components.animation_script.animation_leaf import AnimationLeaf
logger = CustomLogger.getLogger(__name__)


TITLE = 'Delete Node in a Linked List'
STATEMENT = (
    'Write a function to delete a node in a singly linked list. You will not be given access to the head'
    ' of the list, instead you will be given access to the node to be deleted directly.'
)
CONSTRAINTS = []
CONSTRAINTS.append(
    'The number of nodes in the given list is in the range [2, 1000]',
)
CONSTRAINTS.append(r'-1000 $\leq$ Node.val $\leq$ 1000')
CONSTRAINTS.append('The value of each node in the list is unique')
CONSTRAINTS.append(
    'The node to be deleted is in the list and is not a tail node',
)


class BasePresentProblem(BaseScene):
    def __init__(
        self,
        title=TITLE,
        statement_header='Statement',
        statement=STATEMENT,
        constraints_header='Constraints',
        constraints=CONSTRAINTS,
        problem_dir=None,
        aligned_animation_scene=None,
    ):
        super().__init__(
            problem_dir=problem_dir,
            aligned_animation_scene=aligned_animation_scene,
        )
        # BaseScene.__init__(self, problem_dir=problem_dir, aligned_animation_scene=aligned_animation_scene)
        self._title = ProblemText.create_title(title)
        self._statement_header = ProblemText.create_header(statement_header)
        self._statement = ProblemText.create_statement(statement)
        self._constraints_header = ProblemText.create_header(
            constraints_header,
        )
        self._constraints = ProblemText.create_constraints_list(constraints)

        self._animation_spec = self.create_animation_spec()
        self.add_base_animations()

    def create_animation_spec(self) -> dict:
        spec = {
            'title': self.present_problem_title(self.aligned_animation_scene.get_child('title')),
            'statement_header': self.present_problem_statement_header(),
            'statement': self.present_problem_statement(),
            'constraints_header': self.present_problem_constraints_header(),
            'constraints': self._init_constraints_animations(),
        }
        return spec

    def setup(self):
        super().setup()

    def construct(self):
        super().construct()

    def tear_down(self):
        super().tear_down()

    # FIXME
    def _init_constraints_animations(self) -> Callable:
        def inner():
            constraint_animations = []
            for index in range(len(self._constraints)):
                constraint_animations.append(
                    self.present_single_problem_constraint(index=index),
                )
            return constraint_animations
        return inner

    def present_problem_title(self, aligned_animation_section: AnimationLeaf) -> Callable[..., list[Animation]]:
        audio_duration = aligned_animation_section.audio_duration

        def inner() -> list[Animation]:
            fade_in_duration = round(audio_duration * 0.3, 2)
            wait_duration = round(audio_duration * 0.3, 2)
            move_duration = round(
                audio_duration - fade_in_duration - wait_duration, 2,
            )
            move_animation = self._title.animate(
                run_time=move_duration,
            ).to_edge(UP)
            move_animation.run_time = move_duration
            return [
                FadeIn(self._title, run_time=fade_in_duration),
                Wait(run_time=wait_duration),
                move_animation,
            ]
        return inner

    def present_problem_statement_header(self) -> Callable[..., list[Animation]]:
        def inner() -> list[Animation]:
            self._position_element_below_other(
                self._statement_header, self._title,
            )
            return [FadeIn(self._statement_header)]
        return inner

    def present_problem_statement(self) -> Callable[..., list[Animation]]:
        def inner() -> list[Animation]:
            self._position_element_below_other(
                self._statement, self._statement_header,
            )
            return [FadeIn(self._statement)]
        return inner

    def present_problem_constraints_header(self) -> Callable[..., list[Animation]]:
        def inner() -> list[Animation]:
            self._position_element_below_other(
                self._constraints_header, self._statement,
            )
            return [FadeIn(self._constraints_header)]
        return inner

    def present_single_problem_constraint(self, index) -> Callable[..., list[Animation]]:
        def inner() -> list[Animation]:
            self._position_element_below_other(
                self._constraints, self._constraints_header,
            )
            return [FadeIn(self._constraints[index])]
        return inner

    def _position_element_below_other(self, element, other):
        element.next_to(other, DOWN)
        element.to_edge(LEFT)
