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
from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.leetcode.problem_text import ProblemText
# from code_curator.base_scene import run_time_can_be_truncated
from code_curator.animations.utils.utils import run_time_can_be_truncated

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


class BasePresentProblem:
    def __init__(
        self,
        title="",
        statement_header="Statement",
        statement="",
        constraints_header="Constraints",
        constraints=None,
        scene=None,
        **kwargs,
    ):
        # super().__init__(
        #     problem_dir=problem_dir,
        #     aligned_animation_scene=aligned_animation_scene,
        #     **kwargs,
        # )
        self.title_tex = self._create_title(title)
        self.statement_header_tex = self._create_statement_header(statement_header)
        self.statement_tex = self._create_statement(statement)
        self.constraints_header_tex = self._create_constraints_header(constraints_header)
        self.constraints_tex = self._create_constraints(constraints)
        self.scene = scene

    @property
    def mobjects(self):
        return self.scene.mobjects

    @run_time_can_be_truncated
    def fade_in_title(self):
        return FadeIn(self.title_tex)

    def move_title(self):
        return self.title_tex.animate.to_edge(UP)

    def statement_header(self):
        self._position_element_below_lowest_in_scene(
            self.statement_header_tex,
        )
        return FadeIn(self.statement_header_tex)

    def statement(self):
        self._position_element_below_lowest_in_scene(
            self.statement_tex,
        )
        return FadeIn(self.statement_tex)

    def constraints_header(self):
        self._position_element_below_lowest_in_scene(
            self.constraints_header_tex,
        )
        return FadeIn(self.constraints_header_tex)

    def constraint_one(self):
        self._position_element_below_lowest_in_scene(
            self.constraints_tex,
        )
        return FadeIn(self.constraints_tex[0])

    def constraint_two(self):
        return FadeIn(self.constraints_tex[1])

    def constraint_three(self):
        return FadeIn(self.constraints_tex[2])

    def constraint_four(self):
        return FadeIn(self.constraints_tex[3])

    class constraints(AnimationGenerator):
        def zero(self):
            self._position_element_below_lowest_in_scene(
                self.constraints,
            )
            yield FadeIn(self.constraints[0])

        def one(self):
            yield FadeIn(self.constraints[1])

        def two(self):
            yield FadeIn(self.constraints[2])

        def three(self):
            yield FadeIn(self.constraints[3])

    def get_constraint_tex(self, num: int) -> Tex:
        """Retrieve ``Tex`` for constraint ``num``.

        Args:
            num: Number of constraint

        Returns:
            Constraint ``Tex``
        """
        return self.constraints_tex[num - 1]

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
    ) -> None:
        """Positions ``element`` below the current lowest mobject in the scene.

        Args:
            element: Mobject to be placed the lowest.
        """
        # NOTE: All scenes will now contain just one Mobject with submobjects
        mobjects_by_height = sorted(self.mobjects[0].submobjects, key=lambda mob: mob.get_center()[1])
        if mobjects_by_height[0] is element:
            lowest_mobject = mobjects_by_height[1]
        else:
            lowest_mobject = mobjects_by_height[0]

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
