from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from .subanimations.wave_pointer import WavePointer
from .subanimations.shrink_pointer import ShrinkPointer
from .subanimations.move_trav import MoveTrav
from code_curator.data_structures.pointers.pointer import Pointer
from ..data_structure_animation import DataStructureAnimation
from ..utils.math_ import value_from_range_to_range
from code_curator.data_structures.edges.singly_directed_edge import SinglyDirectedEdge
from .subanimations.base_subanimation import BaseSubanimation
# from ..subanimation_group import SubanimationGroup


if TYPE_CHECKING:
    from code_curator.data_structures.singly_linked_list import SinglyLinkedList
    from manim import Scene


class Animator:
    def __init__(self, *, sll: SinglyLinkedList) -> None:
        self.sll = sll
        self.animation_groups: list[list[BaseAnimation]] = [[]]
        self.group_starting_alphas = [0] + [1 / (len(self.animation_groups) - index) for index, _ in enumerate(self.animation_groups)]

    def build(self) -> DataStructureAnimation:
        self._forecast_animations()
        return DataStructureAnimation(self.sll, self)

    @property
    def run_time(self) -> float:
        run_time: float = 0.0
        for group in self.animation_groups:
            run_time += max([anim.run_time for anim in group])

        return run_time

    def interpolate(self, alpha: float) -> None:
        group, converted_alpha = self._get_group_and_alpha(alpha=alpha)
        for animation in group:
            animation.interpolate(converted_alpha)

    def _get_group_and_alpha(self, alpha: float):
        for i, curr_start_alpha in enumerate(self.group_starting_alphas):
            if i == 0:
                continue

            prev_start_alpha = self.group_starting_alphas[i - 1]

            if alpha < curr_start_alpha:
                return (
                    self.animation_groups[i - 1],
                    value_from_range_to_range(
                        value=alpha,
                        init_min=prev_start_alpha,
                        init_max=curr_start_alpha,
                        new_min=0,
                        new_max=1,
                    ),
                )


    def clean_up_from_scene(self, scene: Scene) -> None:
        for animation in itertools.chain.from_iterable(self.animation_groups):
            animation.clean_up_from_scene(scene)

        self.animation_groups = [[]]

    def _forecast_animations(self):
        # Create successive groups
        successive_animations_groups = []
        for group in self.animation_groups:
            successive_animations_groups.append([])
            for animation in group:
                successive_animations_groups[-1].append(
                    animation.create_successive_counterpart()
                )

        # Run each group and assign terminal sll to non-successive counterparts
        for actual_group, successive_group in zip(self.animation_groups, successive_animations_groups):
            for forecast_animation in successive_group:
                forecast_animation.begin()
                forecast_animation.interpolate(1)
                forecast_animation.clean_up_from_animation()

            for actual_animation, forecast_animation in zip(actual_group, successive_group):
                actual_animation.sll_post_subanimation_group = forecast_animation._sll.copy()
                actual_animation.finished_subanimation = forecast_animation.copy()

    def create_new_grouping(self) -> None:
        if not self.animation_groups[-1]:
            raise RuntimeError("You must add at least one animation before creating a new grouping.")

        self.animation_groups.append([])

    def advance_pointer(
        self,
        pointer: Pointer,
        /,
        *,
        num_nodes: int = 1,
        continuous: bool = False,
        run_time: float = 1.0,
    ):
        return self._add_animation(
            MoveTrav(
                sll=self.sll,
                trav=pointer,
                to_node=self.sll[self.sll._nodes.index(pointer.node) + num_nodes],
                run_time=run_time,
            )
        )

    def wave_pointer(
            self,
            pointer: SinglyDirectedEdge,
            /, *,
            run_time: float,
            num_waves: int = 1,
    ):
        return self._add_animation(
            WavePointer(
                sll=self.sll,
                pointer=pointer,
                run_time=run_time,
                num_waves=num_waves,
            )
        )

    def shrink_pointer(
        self,
        pointer: SinglyDirectedEdge,
        /,
        *,
        run_time: float,
    ) -> SinglyLinkedList:
        return self._add_animation(
            ShrinkPointer(
                sll=self.sll,
                pointer=pointer,
                node=pointer._,
                run_time=run_time,
            )
        )

    def _add_animation(self, animation):
        self.animation_groups[-1].append(animation)
        return self.sll
