"""
TODO.
- Allow person to put in basic text and have parser
  convert it to something that's readable by Tex
"""
from __future__ import annotations

from manim import BulletedList
from manim import DOWN
from manim import FadeIn
from manim import LEFT
from manim import Mobject
from manim import Tex
from manim import UP
from manim import Wait

from code_curator.animations.animation_generator import AnimationGenerator
from code_curator.animations.fixed_succession import FixedSuccession
from code_curator.base_scene import BaseScene
from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.leetcode.problem_text import ProblemText

logger = CustomLogger.getLogger(__name__)


TITLE = "Delete Node in a Linked List"
STATEMENT = (
    "Write a function to delete a node in a singly linked list. You will not be given"
    " access to the head of the list, instead you will be given access to the node to"
    " be deleted directly."
)
CONSTRAINTS = []
CONSTRAINTS.append(
    "The number of nodes in the given list is in the range [2, 1000]",
)
CONSTRAINTS.append(r"-1000 $\leq$ Node.val $\leq$ 1000")
CONSTRAINTS.append("The value of each node in the list is unique")
CONSTRAINTS.append(
    "The node to be deleted is in the list and is not a tail node",
)


class BasePresentProblem(BaseScene):
    def __init__(
        self,
        title=TITLE,
        statement_header="Statement",
        statement=STATEMENT,
        constraints_header="Constraints",
        constraints=CONSTRAINTS,
        problem_dir=None,
        aligned_animation_scene=None,
        **kwargs,
    ):
        super().__init__(
            problem_dir=problem_dir,
            aligned_animation_scene=aligned_animation_scene,
            **kwargs,
        )
        self._title = self._create_title(title)
        self._statement_header = self._create_statement_header(statement_header)
        self._statement = self._create_statement(statement)
        self._constraints_header = self._create_constraints_header(constraints_header)
        self._constraints = self._create_constraints(constraints)

    def fade_in_title(self):
        yield FadeIn(self._title)

    def move_title(self):
        self._title.to_edge(UP)
        yield Wait()
        # yield self._title.animate.to_edge(UP)

    def statement_header(self):
        self._position_element_below_lowest_in_scene(
            self._statement_header,
            fall_back=self._title,
        )
        yield FadeIn(self._statement_header)

    def statement(self):
        self._position_element_below_lowest_in_scene(
            self._statement,
            fall_back=self._statement_header,
        )
        yield FadeIn(self._statement)

    def constraints_header(self):
        self._position_element_below_lowest_in_scene(
            self._constraints_header,
            fall_back=self._statement_header,
        )
        yield FadeIn(self._constraints_header)

    class constraints(AnimationGenerator):
        def zero(self):
            self._position_element_below_lowest_in_scene(
                self._constraints,
                fall_back=self._constraints_header,
            )
            yield FadeIn(self._constraints[0])

        def one(self):
            yield FadeIn(self._constraints[1])

        def two(self):
            yield FadeIn(self._constraints[2])

        def three(self):
            yield FadeIn(self._constraints[3])

    def get_constraint_tex(self, num: int) -> Tex:
        """Retrieve ``Tex`` for constraint ``num``.

        Args:
            num: Number of constraint

        Returns:
            Constraint ``Tex``
        """
        return self._constraints[num - 1]

    def _create_exclude_none_kwargs(self, **kwargs) -> dict:
        for key, value in kwargs.copy().items():
            if value is None:
                del kwargs[key]

        return kwargs

    def _position_element_below_other(self, element: Mobject, other: Mobject) -> None:
        """Place ``element`` below ``other``.

        Args:
            element: Element to be placed below.
            other: Reference Mobject for placement.
        """
        element.next_to(other, DOWN)
        element.to_edge(LEFT)

    def _position_element_below_lowest_in_scene(
        self,
        element: Mobject,
        *,
        fall_back: Mobject | None = None,
    ) -> None:
        """Positions ``element`` below the current lowest mobject in the scene.

        Args:
            element: Mobject to be placed the lowest.
            fall_back:
                Mobject to be used as reference if lowest Mobject can't be found/used.
        """
        try:
            mobjects_by_height = sorted(
                self.mobjects,
                key=lambda mob: mob.get_center()[1],
            )
            lowest_mobject = [
                mob
                for mob in mobjects_by_height
                if type(mob) != Mobject and mob is not element  # noqa: E721
            ][0]
        except IndexError:
            # No mobjects in scene yet. This is expected.
            if fall_back is None or not self.mobjects:
                return

            try:
                lowest_mobject = [
                    mob
                    for mob in mobjects_by_height
                    if type(mob) != Mobject  # noqa: E721
                ][0]
            except IndexError:
                # All mobjects in the scene are of type Mobject
                # study this (this might not be a big deal at all)
                breakpoint()
            else:
                self._position_element_below_other(element, fall_back)
        else:
            self._position_element_below_other(element, lowest_mobject)

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

    def _create_constraints_header(
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

    def _create_constraints(
        self,
        constraints: list[str],
        font_size: int | None = None,
        color: str | None = None,
        dot_scale_factor: float | None = None,
        buff: float | None = None,
        **kwargs,
    ) -> BulletedList:
        kwargs.update(
            self._create_exclude_none_kwargs(
                font_size=font_size,
                color=color,
                dot_scale_factor=dot_scale_factor,
                buff=buff,
            ),
        )
        return ProblemText.create_constraints_list(constraints, **kwargs)
