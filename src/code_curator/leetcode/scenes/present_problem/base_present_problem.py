'''
TODO
- Allow person to put in basic text and have parser convert it to something that's readable by Tex
'''
from __future__ import annotations

from collections.abc import Callable

from code_curator.animations.fixed_succession import FixedSuccession
from code_curator.base_scene import BaseScene
from code_curator.constants import DEFAULT_MOBJECT_COLOR
from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.leetcode.problem_text import ProblemText
from manim import Animation
from manim import BulletedList
from manim import DOWN
from manim import FadeIn
from manim import LEFT
from manim import Mobject
from manim import UP
from manim import Wait
from code_curator.script_handling.components.animation_script.animation_leaf import AnimationLeaf
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
        self._title = self._create_title(title)
        self._statement_header = self._create_statement_header(statement_header)
        self._statement = self._create_statement(statement)
        self._constraints_header = self._create_constraints_header(constraints_header)
        self._constraints = self._create_constraints(constraints)
        # self._title = ProblemText.create_title(title)
        # self._statement_header = ProblemText.create_header(statement_header)
        # self._statement = ProblemText.create_statement(statement)
        # self._constraints_header = ProblemText.create_header(
        #     constraints_header,
        # )
        # self._constraints = ProblemText.create_constraints_list(constraints)

        self._animation_spec = self.create_animation_spec()
        self.add_base_animations()

    def _create_title(
        self,
        text: str,
        color: str | None = None,
        **kwargs,
    ) -> ProblemText:
        kwargs.update(
            self._create_exclude_none_kwargs(
                color=color,
            ),
        )
        return ProblemText.create_title(text, **kwargs)

    def _create_statement_header(
        self,
        text: str,
        font_size: int | None = None,
        color: str | None = None,
        **kwargs,
    ) -> ProblemText:
        kwargs.update(
            self._create_exclude_none_kwargs(
                font_size=font_size,
                color=color,
            ),
        )
        return ProblemText.create_header(text, **kwargs)

    def _create_statement(
        self,
        text: str,
        font_size: int | None = None,
        color: str | None = None,
        **kwargs,
    ) -> ProblemText:
        kwargs.update(
            self._create_exclude_none_kwargs(
                font_size=font_size,
                color=color,
            ),
        )
        return ProblemText.create_statement(text, **kwargs)

    def _create_constraints_header(self, text: str, font_size: int | None = None, color: str | None = None, **kwargs) -> ProblemText:
        kwargs.update(
            self._create_exclude_none_kwargs(
                font_size=font_size,
                color=color,
            ),
        )
        return ProblemText.create_header(text, **kwargs)

    def _create_constraints(self, constraints: list[str], font_size: int | None = None, color: str | None = None, dot_scale_factor: float | None = None, buff: float | None = None, **kwargs) -> BulletedList:
        kwargs.update(
            self._create_exclude_none_kwargs(
                font_size=font_size,
                color=color,
                dot_scale_factor=dot_scale_factor,
                buff=buff,
            ),
        )
        return ProblemText.create_constraints_list(constraints, **kwargs)

    def _create_exclude_none_kwargs(self, **kwargs) -> dict:
        for key, value in kwargs.copy().items():
            if value is None:
                del kwargs[key]

        return kwargs

    def create_animation_spec(self) -> dict:
        return {
            'title': self.present_title(),
            'statement_header': self.present_statement_header(),
            'statement': self.present_statement(),
            'constraints_header': self.present_constraints_header(),
            'constraints': self._init_constraints_animations(),
        }

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

    def present_title(self) -> Callable[..., list[Animation]]:
        def title() -> list[Animation]:
            audio_duration = self.title['run_time']
            fade_in_duration = round(audio_duration * 0.2, 2)
            wait_duration = round(audio_duration * 0.2, 2)
            move_duration = round(
                audio_duration - fade_in_duration - wait_duration, 2,
            )
            move_animation = self._title.animate(
                run_time=move_duration,
            ).to_edge(UP)
            move_animation.run_time = move_duration
            return [
                FixedSuccession(
                    FadeIn(self._title, run_time=fade_in_duration),
                    Wait(run_time=wait_duration),
                    move_animation,
                ),
            ]
        return title

    def present_statement_header(self) -> Callable[..., list[Animation]]:
        def statement_header() -> list[Animation]:
            self._position_element_below_lowest_in_scene(self._statement_header, fall_back=self._title)
            return [FadeIn(self._statement_header)]
        return statement_header

    def present_statement(self) -> Callable[..., list[Animation]]:
        def statement() -> list[Animation]:
            self._position_element_below_lowest_in_scene(self._statement, fall_back=self._statement_header)
            return [FadeIn(self._statement)]
        return statement

    def present_constraints_header(self) -> Callable[..., list[Animation]]:
        def constraints_header() -> list[Animation]:
            self._position_element_below_lowest_in_scene(self._constraints_header, fall_back=self._statement_header)
            return [FadeIn(self._constraints_header)]
        return constraints_header

    def present_single_problem_constraint(self, index) -> Callable[..., list[Animation]]:
        def inner() -> list[Animation]:
            if index == 0:
                self._position_element_below_lowest_in_scene(self._constraints, fall_back=self._constraints_header)

            return [FadeIn(self._constraints[index])]
        return inner

    def _position_element_below_other(self, element, other):
        element.next_to(other, DOWN)
        element.to_edge(LEFT)

    def add_overriding_animation(self, method):
        self._add_animation(method, is_overriding_animation=True)

    def add_nonoverriding_animation(self, method):
        self._add_animation(method, is_overriding_animation=False)

    def _add_animation(self, method, *, is_overriding_animation: bool) -> None:
        self._aligned_animation_scene.add_animation(
            unique_id=method.__name__,
            func=method,
            animation=method(),
            is_overriding_animation=is_overriding_animation,
        )

    def _position_element_below_lowest_in_scene(
        self,
        element: Mobject,
        *,
        fall_back: Mobject | None = None,
    ) -> None:
        try:
            mobjects_by_height = sorted(self.mobjects, key=lambda mob : mob.get_center()[1])
            lowest_mobject = [mob for mob in mobjects_by_height if type(mob) != Mobject and mob is not element][0]
        except IndexError:
            # No mobjects in scene yet. This is expected.
            if fall_back is None or not self.mobjects:
                return

            try:
                lowest_mobject = [mob for mob in mobjects_by_height if type(mob) != Mobject][0]
            except IndexError:
                # All mobjects in the scene are of type Mobject, study this (this might not be a big deal at all)
                breakpoint()
            else:
                self._position_element_below_other(element, fall_back)
        else:
            self._position_element_below_other(element, lowest_mobject)
