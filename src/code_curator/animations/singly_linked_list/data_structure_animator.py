from __future__ import annotations

import inspect
import typing
from collections.abc import Callable
from types import MethodType
from typing import Any
from typing import TYPE_CHECKING

from code_curator.custom_logging.custom_logger import CustomLogger

from ..data_structure_animation import DataStructureAnimation
from ..subanimation_group import SubanimationGroup
from .animation_forecasting.sll_animation_forecaster import SLLAnimationForecaster
from .subanimations.base_subanimation import BaseSubanimation
from animations.subanimations.wait import WaitSubanimation
logger = CustomLogger.getLogger(__name__)

if TYPE_CHECKING:
    from code_curator.data_structures.singly_linked_list import SinglyLinkedList


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
            parent=None,
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
        del self._sub_class_init_kwargs['node']
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
    
    def _get_last_non_wait_padding_subanimation_group(self) -> SubanimationGroup:
        # breakpoint()
        for subanimation in reversed(self._subanimation_group._subanimations):
            if subanimation.is_wait_padding():
                continue
            return subanimation
        raise LookupError(f'Unable to find last non wait padding subanimation group in {self._subanimation_group}')

    def _add_subanimation_concurrently(self, *subanimations_to_add: BaseSubanimation, run_time: float = 1) -> DataStructureAnimator:
        # Get last SubanimationGroup that's not just WaitSubanimation
        # NOTE: We're going to assume that if the previous SubanimationGroup is WaitSubanimation, then one before that isn't
        # because all sequential WaitSubanimations should be consolidated
        last_non_wait_padding_subanimation_group = self._get_last_non_wait_padding_subanimation_group()
        if last_non_wait_padding_subanimation_group.is_successive_group():
            last_non_wait_padding_subanimation_group.lag_ratio = 0

        # if self._last_subanimation_group_is_successive():
        #     self._subanimation_group.get(-1).lag_ratio = 0

        # subanimation_group_id = '_'.join(inspect.stack()[1].function.split('_')[1:]).strip()
        if len(subanimations_to_add) > 1:
            raise ValueError("I don't think more than one subanimation should be allowed here?")

        # for subanimation in subanimations_to_add:
        #     self._subanimation_group.get(-1).add(subanimation)
        for subanimation in subanimations_to_add:
            last_non_wait_padding_subanimation_group.add(subanimation)
            # if not self._subanimation_group.unique_id:
            #     self._subanimation_group.unique_id = subanimation_group_id
        return self

    def _add_subanimation_successively(self, *subanimations_to_add: BaseSubanimation, timing_info: dict | None = None) -> DataStructureAnimator:
        # raise Exception(inspect.stack()[1].function)
        # subanimation_group_id = '_'.join(inspect.stack()[1].function.split('_')[1:]).strip()
        if len(subanimations_to_add) > 1:
            raise ValueError("I don't think more than one subanimation should be allowed here?")
        
        if timing_info is None:
            self._subanimation_group.add(
                *[
                    SubanimationGroup(subanimation, lag_ratio=1)
                    for subanimation in subanimations_to_add
                ],
            )
        else:
            self._subanimation_group.add(
                *[
                    SubanimationGroup(subanimation, lag_ratio=1)
                    for subanimation in subanimations_to_add
                ],
                SubanimationGroup(
                    WaitSubanimation(
                        sll=self._sll,
                        run_time=timing_info['run_time'],
                    ),
                    lag_ratio=1,
                    run_time=timing_info['run_time'],
                    parent=self._subanimation_group,
                )
            )
        
        # breakpoint()
        return self

    def create_subanimation_group_successive_counterpart(self) -> SubanimationGroup:
        return self._subanimation_group.sub_in_successive_counterparts()

    def _last_subanimation_group_is_successive(self) -> bool:
        try:
            last_subanimation = self._subanimation_group.get(-1)
            return last_subanimation.lag_ratio == 1
        except IndexError:
            return False

    def _prepend_subanimation(self, subanimation: BaseSubanimation) -> None:
        subanimation.parent = self._subanimation_group
        self._subanimation_group.insert(0, subanimation)

    def get_subanimation_group(self) -> SubanimationGroup:
        return self._subanimation_group

    def get_run_time(self) -> float:
        return self._subanimation_group.get_run_time()


# FIXME: FIX THIS!!!
@typing.no_type_check
def _register_subanimation(builder_helper_func):
    def inner(self, *args, **kwargs):
        builder_helper_func.args = args
        builder_helper_func.kwargs = kwargs
        self._requested_subanimation_builder_helpers.append(
            builder_helper_func,
        )
        return builder_helper_func(self, *args, **kwargs)
    return inner
