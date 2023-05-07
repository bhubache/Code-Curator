from __future__ import annotations

import typing
from collections.abc import Callable
from types import MethodType
from typing import Any
from typing import TYPE_CHECKING

from custom_logging.custom_logger import CustomLogger

from ..data_structure_animation import DataStructureAnimation
from ..subanimation_group import SubanimationGroup
from .animation_forecasting.sll_animation_forecaster import SLLAnimationForecaster
from .subanimations.base_subanimation import BaseSubanimation
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from data_structures.singly_linked_list import SinglyLinkedList


class DataStructureAnimator:
    def __init__(
        self,
        sll: SinglyLinkedList,
        sll_calling_method: MethodType,
        **sub_class_init_kwargs: Any,
    ) -> None:
        self._sll: SinglyLinkedList = sll
        self._sll_calling_method: MethodType = sll_calling_method
        self._sub_class_init_kwargs: dict[Any, Any] = sub_class_init_kwargs
        self._requested_subanimation_builder_helpers: list[
            Callable[
                [
                    DataStructureAnimator, Any, Any,
                ], DataStructureAnimator,
            ]
        ] = []
        self._subanimation_group: SubanimationGroup = SubanimationGroup(
            lag_ratio=1,
        )

    # TODO: Make abstract
    def clean_up_mobject(self) -> None:
        pass

    def build_animation(self) -> DataStructureAnimation:
        self.__forecast_subanimations()
        return DataStructureAnimation(self._sll, self)

    def __forecast_subanimations(self) -> None:
        lookahead_forecaster = self.__create_sll_animation_forecaster()
        lookahead_forecaster.forecast_animations()

    def __create_sll_animation_forecaster(self) -> SLLAnimationForecaster:
        sll_to_forecast = self._get_sll_to_forecast()
        return SLLAnimationForecaster(
            sll=sll_to_forecast,
            animator_copy=self._sll_calling_method.__func__(
                sll_to_forecast, **self._sub_class_init_kwargs,
            ),
            requested_subanimation_builder_helpers=self._requested_subanimation_builder_helpers,
            true_subanimation_group=self._subanimation_group,
        )

    def _get_sll_to_forecast(self) -> SinglyLinkedList:
        raise NotImplementedError()

    def _add_subanimation_concurrently(self, *subanimations_to_add: BaseSubanimation) -> DataStructureAnimator:
        if self._last_subanimation_group_is_successive():
            self._subanimation_group.get(-1).lag_ratio = 0

        for subanimation in subanimations_to_add:
            self._subanimation_group.get(-1).add(subanimation)
        return self

    def _add_subanimation_successively(self, *subanimations_to_add: BaseSubanimation) -> DataStructureAnimator:
        self._subanimation_group.add(
            *[
                SubanimationGroup(subanimation, lag_ratio=1)
                for subanimation in subanimations_to_add
            ],
        )
        return self

    def create_subanimation_group_successive_counterpart(self) -> SubanimationGroup:
        return self._subanimation_group.sub_in_successive_counterparts()

    def _last_subanimation_group_is_successive(self) -> bool:
        last_subanimation = self._subanimation_group.get(-1)
        return last_subanimation.lag_ratio == 1

    def _prepend_subanimation(self, subanimation: BaseSubanimation) -> None:
        self._subanimation_group.insert(0, subanimation)

    def get_subanimation_group(self) -> SubanimationGroup:
        return self._subanimation_group

    def get_run_time(self) -> float:
        return self._subanimation_group.get_run_time()


# FIXME: FIX THIS!!!
@typing.no_type_check
def _register_subanimation(builder_helper_func):
    def inner(self, *args, **kwargs):
        self._requested_subanimation_builder_helpers.append(
            builder_helper_func,
        )
        return builder_helper_func(self, *args, **kwargs)
    return inner
