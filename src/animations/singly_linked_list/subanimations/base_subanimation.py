from __future__ import annotations

import copy
from abc import ABC
from abc import abstractmethod

from src.custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)


class BaseSubanimation(ABC):
    def __init__(self, run_time: float = 1) -> None:
        self._run_time: float = run_time
        self._sll_post_subanimation_group = None
        self._lag_ratio: float = 0

        self._visited: bool = False
        self._has_started: bool = False

    def __len__(self):
        return 1

    def get_run_time(self) -> float:
        return self._run_time

    def _build_subanimations_with_timings(self) -> float:
        pass

    def copy(self) -> BaseSubanimation:
        return copy.deepcopy(self)

    def begin(self):
        pass

    def get_num_subanimations(self) -> int:
        return len(self)

    @abstractmethod
    def interpolate(self, alpha: float):
        pass

    def clean_up_from_scene(self, scene):
        pass

    @abstractmethod
    def create_successive_counterpart(self) -> BaseSubanimation:
        pass

    def _build_subanimations_with_timings_helper(self):
        pass

    def add(self, subanimation: BaseSubanimation) -> None:
        raise Exception('Can\'t add subanimation to BaseSubanimation')

    @property
    def sll_post_subanimation_group(self):
        return self._sll_post_subanimation_group

    @sll_post_subanimation_group.setter
    def sll_post_subanimation_group(self, sll) -> None:
        self._sll_post_subanimation_group = sll

    @property
    def lag_ratio(self) -> float:
        return 0

    @lag_ratio.setter
    def lag_ratio(self, new_lag_ratio: float) -> None:
        self._lag_ratio = new_lag_ratio
