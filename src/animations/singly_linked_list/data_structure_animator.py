from __future__ import annotations
from types import MethodType

from .animation_forecasting.sll_animation_forecaster import SLLAnimationForecaster
from ..subanimation_group import SubanimationGroup
from ..data_structure_animation import DataStructureAnimation
from .subanimations.base_subanimation import BaseSubanimation

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)


class DataStructureAnimator:
    def __init__(self, sll, sll_calling_method, **sub_class_init_kwargs):
        self._sll = sll
        self._sll_calling_method = sll_calling_method
        self._sub_class_init_kwargs: dict = sub_class_init_kwargs
        self._requested_subanimation_builder_helpers: list[MethodType] = []
        self._subanimation_group: SubanimationGroup = SubanimationGroup(lag_ratio=1)

    # TODO: Make abstract
    def clean_up_mobject(self):
        pass

    def build_animation(self) -> DataStructureAnimation:
        self.__forecast_subanimations()
        return DataStructureAnimation(self._sll, self)

    def __forecast_subanimations(self):
        lookahead_forecaster = self.__create_sll_animation_forecaster()
        lookahead_forecaster.forecast_animations()

    def __create_sll_animation_forecaster(self) -> DataStructureAnimator:
        sll_copy = self._sll.copy()
        return SLLAnimationForecaster(
            sll=sll_copy,
            animator_copy=self._sll_calling_method.__func__(sll_copy, **self._sub_class_init_kwargs),
            requested_subanimation_builder_helpers=self._requested_subanimation_builder_helpers,
            true_subanimation_group=self._subanimation_group
        )

    def __add_subanimation_concurrently(self, *subanimations_to_add: BaseSubanimation):
        if self._last_subanimation_group_is_successive():
            self._subanimation_group.get(-1)._lag_ratio = 0

        for subanimation in subanimations_to_add:
            self._subanimation_group.get(-1).add(subanimation)
        return self

    def __add_subanimation_successively(self, *subanimations_to_add: BaseSubanimation):
        self._subanimation_group.add(
            *[SubanimationGroup(subanimation, lag_ratio=1) for subanimation in subanimations_to_add]
        )
        return self

    def create_subanimation_group_successive_counterpart(self) -> SubanimationGroup:
        return self._subanimation_group.sub_in_successive_counterparts()

    def _last_subanimation_group_is_successive(self) -> bool:
        last_subanimation = self._subanimation_group.get(-1)
        return last_subanimation._lag_ratio == 1

    def _prepend_subanimation(self, subanimation: BaseSubanimation) -> None:
        self._subanimation_group.insert(0, subanimation)

    def get_subanimation_group(self) -> list[list[BaseSubanimation]]:
        return self._subanimation_group

    def get_run_time(self) -> float:
        return self._subanimation_group.get_run_time()

    def _register_subanimation(builder_helper_func):
        def inner(self: DataStructureAnimator, *args, **kwargs):
            self._requested_subanimation_builder_helpers.append(builder_helper_func)
            return builder_helper_func(self, *args, **kwargs)
        return inner

    @_register_subanimation
    def with_fade_out_container(self):
        return self.__add_subanimation_concurrently(self._create_fade_out_container())

    @_register_subanimation
    def subsequently_fade_out_container(self):
        return self.__add_subanimation_successively(self._create_fade_out_container())

    @_register_subanimation
    def with_fade_out_pointer(self):
        return self.__add_subanimation_concurrently(self._create_fade_out_pointer())

    @_register_subanimation
    def subsequently_fade_out_pointer(self):
        return self.__add_subanimation_successively(self._create_fade_out_pointer())

    @_register_subanimation
    def with_shrink_pointer(self):
        return self.__add_subanimation_concurrently(self._create_shrink_pointer())

    @_register_subanimation
    def subsequently_shrink_pointer(self):
        return self.__add_subanimation_successively(self._create_shrink_pointer())

    @_register_subanimation
    def with_unshrink_pointer(self):
        return self.__add_subanimation_concurrently(self._create_unshrink_pointer())

    @_register_subanimation
    def subsequently_unshrink_pointer(self):
        return self.__add_subanimation_successively(self._create_unshrink_pointer())

    @_register_subanimation
    def with_curve_pointer(self):
        return self.__add_subanimation_concurrently(self._create_curve_pointer())

    @_register_subanimation
    def subsequently_curve_pointer(self):
        return self.__add_subanimation_successively(self._create_curve_pointer())

    @_register_subanimation
    def with_center_sll(self):
        return self.__add_subanimation_concurrently(self._create_center_sll())

    @_register_subanimation
    def subsequently_center_sll(self):
        return self.__add_subanimation_successively(self._create_center_sll())

    @_register_subanimation
    def with_flatten_list(self):
        return self.__add_subanimation_concurrently(self._create_flatten_list())

    @_register_subanimation
    def subsequently_flatten_list(self):
        return self.__add_subanimation_successively(self._create_flatten_list())

    @_register_subanimation
    def with_fade_out_first_temp_trav(self):
        return self.__add_subanimation_concurrently(self._create_fade_out_first_temp_trav())

    @_register_subanimation
    def subsequently_fade_out_first_temp_trav(self):
        return self.__add_subanimation_successively(self._create_fade_out_first_temp_trav())

    @_register_subanimation
    def with_fade_out_second_temp_trav(self):
        return self.__add_subanimation_concurrently(self._create_fade_out_second_temp_trav())

    @_register_subanimation
    def subsequently_fade_out_second_temp_trav(self):
        return self.__add_subanimation_successively(self._create_fade_out_second_temp_trav())

    @_register_subanimation
    def with_fade_in_container(self):
        return self.__add_subanimation_concurrently(self._create_fade_in_container())

    @_register_subanimation
    def subsequently_fade_in_container(self):
        return self.__add_subanimation_successively(self._create_fade_in_container())

    @_register_subanimation
    def with_fade_in_pointer(self):
        return self.__add_subanimation_concurrently(self._create_fade_in_pointer())

    @_register_subanimation
    def subsequently_fade_in_pointer(self):
        return self.__add_subanimation_successively(self._create_fade_in_pointer())

    @_register_subanimation
    def with_change_prev_node_pointer(self):
        return self.__add_subanimation_concurrently(self._create_change_prev_node_pointer())

    @_register_subanimation
    def subsequently_change_prev_node_pointer(self):
        return self.__add_subanimation_successively(self._create_change_prev_node_pointer())

    @_register_subanimation
    def with_shift_sub_list(self):
        return self.__add_subanimation_concurrently(self._create_shift_sub_list())

    @_register_subanimation
    def subsequently_shift_sub_list(self):
        return self.__add_subanimation_successively(self._create_shift_sub_list())
