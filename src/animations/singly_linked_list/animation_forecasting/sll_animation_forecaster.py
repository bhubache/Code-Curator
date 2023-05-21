from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from custom_logging.custom_logger import CustomLogger

from ...subanimation_group import SubanimationGroup
from ..subanimations.base_subanimation import BaseSubanimation
from ..subanimations.leaf_subanimation import LeafSubanimation
from .forecasted_subanimation_group_creator import ForecastedSubanimationGroupCreator
from .interdependent_subanimation_finder import InterdependentSubanimationFinder
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from data_structures.singly_linked_list import SinglyLinkedList
    from ..data_structure_animator import DataStructureAnimator

# TODO: Separate creation of successive package and assigning of forecasted mobjects into their own classes


class SLLAnimationForecaster:
    def __init__(
        self,
        sll: SinglyLinkedList,
        animator_copy: DataStructureAnimator,
        requested_subanimation_builder_helpers: list[Callable],
        true_subanimation_group: SubanimationGroup,
    ) -> None:
        self._sll: SinglyLinkedList = sll
        self._true_subanimation_group: SubanimationGroup = true_subanimation_group
        self._forecasted_subanimation_group = ForecastedSubanimationGroupCreator.create_forecasted_subanimation_group(
            animator_copy, requested_subanimation_builder_helpers,
        )

    def forecast_animations(self) -> None:
        self._sub_in_successive_subanimations_where_possible()
        self._assign_forecasted_subanimations()

        # NOTE: THIS WAS HERE ORIGINALLY!!!
        # self._move_sll_subanimations_to_beginning_of_group()

    def _get_interdependent_subanimations(self) -> LeafSubanimation:
        interdependent_subanimation_finder = InterdependentSubanimationFinder(
            subanimation_group=self._true_subanimation_group,
        )
        return interdependent_subanimation_finder.get_interdependent_subanimations()

    def _no_interdependent_subanimations(self, interdepenent_subanimations: list[LeafSubanimation]) -> bool:
        return len(interdepenent_subanimations) == 0

    def _sub_in_successive_subanimations_where_possible(self) -> None:
        interdependent_subanimations = self._get_interdependent_subanimations()
        for group in self._true_subanimation_group:
            self._sub_in_successive_subanimations_where_possible_helper(
                group, interdependent_subanimations,
            )

    def _sub_in_successive_subanimations_where_possible_helper(
        self,
        group: SubanimationGroup,
        interdependent_subanimations: list[LeafSubanimation],
    ) -> None:
        for i, subanimation in enumerate(group):
            if subanimation not in interdependent_subanimations and isinstance(subanimation, LeafSubanimation):
                group.set(i, subanimation.create_successive_counterpart())

    def _assign_forecasted_subanimations(self) -> None:
        for true_subanimation, forecast_subanimation in zip(
            self._true_subanimation_group,
            self._forecasted_subanimation_group,
        ):
            self._assign_forecasted_subanimations_helper(
                true_subanimation=true_subanimation, forecast_subanimation=forecast_subanimation,
            )

    def _assign_forecasted_subanimations_helper(
        self,
        true_subanimation: BaseSubanimation,
        forecast_subanimation: BaseSubanimation,
    ) -> None:
        assert isinstance(true_subanimation, SubanimationGroup) \
            and isinstance(forecast_subanimation, SubanimationGroup) \
            or isinstance(true_subanimation, LeafSubanimation) \
            and isinstance(forecast_subanimation, LeafSubanimation), 'Hierarchy doesn\'t match'

        if isinstance(true_subanimation, LeafSubanimation):
            forecast_subanimation.begin()
            forecast_subanimation.interpolate(1)
            forecast_subanimation.clean_up_from_animation()
            return

        for true, forecast in zip(true_subanimation, forecast_subanimation):
            self._assign_forecasted_subanimations_helper(
                true_subanimation=true, forecast_subanimation=forecast,
            )

        if isinstance(true_subanimation, SubanimationGroup):
            for true, forecast in zip(true_subanimation, forecast_subanimation):
                if isinstance(true, LeafSubanimation):
                    true.sll_post_subanimation_group = forecast._sll.copy()
                    true.finished_subanimation = forecast.copy()

    # TODO: Check to see if this can be removed
    # def _move_sll_subanimations_to_beginning_of_group(self):
    #     for list_index, subanimation_list in enumerate(self._get_true_subanimation_group()):
    #         sll_subanimations = []
    #         for i, subanimation in enumerate(subanimation_list):
    #             if subanimation._animates_sll:
    #                 sll_subanimations.append(subanimation)

    #         for subanimation in sll_subanimations:
    #             self._true_package.remove_subanimation(group_index=list_index, subanimation=subanimation)
    #             # self._subanimation_lists[list_index].remove(subanimation)

    #         for subanimation in sll_subanimations:
    #             self._true_package.prepend_subanimation(group_index=list_index, subanimation=subanimation)
    #             # self._subanimation_lists[list_index].insert(0, subanimation)

    # def _get_true_subanimation_group(self) -> SubanimationGroup:
    #     return self._true_package.get_subanimation_group()

    # def _set_true_subanimation(self, index: int, subanimation: BaseSubanimation) -> None:
    #     self._true_package.set_subanimation(index=index, subanimation=subanimation)

    # def _get_flattened_true_subanimation_group(self) -> list[LeafSubanimation]:
    #     return list(self._true_package.get_subanimation_group().flatten())

    # def _get_forecasted_subanimation_group(self) -> SubanimationGroup:
    #     return self._forecasted_subanimation_group.get_subanimation_group()
