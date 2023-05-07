from __future__ import annotations

from collections.abc import Iterator

import numpy as np
from custom_logging.custom_logger import CustomLogger
from manim import Scene

from .singly_linked_list.subanimations.base_subanimation import BaseSubanimation
from .singly_linked_list.subanimations.leaf_subanimation import LeafSubanimation
logger = CustomLogger.getLogger(__name__)


class SubanimationGroup(BaseSubanimation):
    def __init__(
        self,
        *subanimations: BaseSubanimation,
        run_time: float = 1,
        lag_ratio: float = 0,
    ) -> None:
        super().__init__()
        self._subanimations: list[BaseSubanimation] = [
            sub for sub in subanimations
        ]
        self._lag_ratio: float = lag_ratio
        self._subanimations_with_timings: list[tuple[BaseSubanimation, float, float]] = [
        ]
        self._run_time: float = run_time
        self.max_end_time: float = 0

    def __str__(self) -> str:
        contents = '\n'.join(
            [
                subanimation._to_str_helper(
                    start_time, end_time, recursion_level=1,
                )
                for subanimation, start_time, end_time in self._subanimations_with_timings
            ],
        )
        return (
            '\n'.join(
                (
                    # f'[lag_ratio: {self._lag_ratio}',
                    f'lag_ratio: {self._lag_ratio}, 0-{self.get_run_time()}, max_end_time: {self.max_end_time}',
                    '[',
                    f'{contents}',
                    ']',
                ),
            )
        )

    def _to_str_helper(self, start_time: float, end_time: float, recursion_level: int) -> str:
        start_color = None
        end_color = '\033[0m'
        RED = '\033[0;31m'
        GREEN = '\033[0;32m'
        BROWN = '\033[0;33m'
        BLUE = '\033[0;34m'
        PURPLE = '\033[0;35m'
        CYAN = '\033[0;36m'
        LIGHT_GRAY = '\033[0;37m'

        if recursion_level == 1:
            start_color = BLUE
        elif recursion_level == 2:
            start_color = GREEN
            end_color = BLUE
        elif recursion_level == 3:
            start_color = BROWN
            end_color = GREEN
        elif recursion_level == 4:
            start_color = RED
            end_color = BROWN
        elif recursion_level == 5:
            start_color = PURPLE
            end_color = RED
        elif recursion_level == 5:
            start_color = CYAN
            end_color = PURPLE
        elif recursion_level == 5:
            start_color = LIGHT_GRAY
            end_color = CYAN

        contents = '\n'.join(
            [
                subanimation._to_str_helper(
                    start_time, end_time, recursion_level=recursion_level + 1,
                )
                for subanimation, start_time, end_time in self._subanimations_with_timings
            ],
        )
        left_padding: str = '  ' * recursion_level
        header: str = (
            f'{start_color}'
            f'{left_padding}'
            f'lag_ratio: {self._lag_ratio}, '
            f'{start_time}-{end_time}: '
            f'max_end_time: {self.max_end_time}'
        )
        return (
            '\n'.join(
                (
                    header,
                    f'{left_padding}[',
                    f'{contents}',
                    f'{left_padding}]{end_color}',
                ),
            )
        )

    def __iter__(self) -> Iterator:
        return self._subanimations.__iter__()

    def __len__(self) -> int:
        total_length: int = 0
        for subanimation in self._subanimations:
            total_length += len(subanimation)
        return total_length

    def __getitem__(self, index: int) -> BaseSubanimation:
        return self._subanimations[index]

    def init_run_time(self) -> None:
        self._build_subanimations_with_timings()
        print(self)

    def begin(self) -> None:
        pass

    def interpolate(self, alpha: float) -> None:
        def clip(sub_alpha: float) -> float:
            START_SUB_ALPHA = 0
            END_SUB_ALPHA = 1

            if sub_alpha < START_SUB_ALPHA:
                return -1000
            elif sub_alpha > END_SUB_ALPHA:
                return 1000
            else:
                return sub_alpha

        time = alpha * self.max_end_time
        for subanimation, start_time, end_time in self._subanimations_with_timings:
            subanimation_run_time: float = end_time - start_time
            sub_alpha: float = 0

            sub_alpha = clip((time - start_time) / subanimation_run_time)

            if self._subanimation_ready_to_begin(subanimation, sub_alpha):
                subanimation.begin()

            if self._subanimation_is_rendering(subanimation, sub_alpha):
                subanimation.interpolate(sub_alpha)

            if self._subanimation_is_complete(subanimation, sub_alpha):
                subanimation.clean_up_from_animation()

    def clean_up_from_animation(self) -> None:
        pass

    def clean_up_from_scene(self, scene: Scene) -> None:
        for subanimation in self._subanimations:
            subanimation.clean_up_from_scene(scene)

    def _build_subanimations_with_timings(self) -> None:
        if isinstance(self, LeafSubanimation):
            return

        if not self._visited:
            self._visited = True
            curr_time: float = 0
            for subanimation in self._subanimations:
                start_time: float = curr_time
                end_time: float = start_time + subanimation.get_run_time()
                self._subanimations_with_timings.append(
                    (subanimation, start_time, end_time),
                )
                curr_time = (1 - self._lag_ratio) * start_time + \
                    self._lag_ratio * end_time

        for child in self._subanimations:
            child._build_subanimations_with_timings()

        self._run_time = self._init_run_time(self._run_time)

    def _init_run_time(self, run_time: float) -> float:
        self.max_end_time: float = 0
        if self._subanimations_with_timings:
            self.max_end_time = np.max(
                [awt[2] for awt in self._subanimations_with_timings],
            )
        return self.max_end_time if run_time is None else run_time

    def _subanimation_ready_to_begin(self, subanimation: BaseSubanimation, sub_alpha: float) -> bool:
        if sub_alpha >= 0 and not subanimation._has_started and isinstance(subanimation, LeafSubanimation):
            subanimation._has_started = True
            return True
        return False

    def _subanimation_is_rendering(self, subanimation: BaseSubanimation, sub_alpha: float) -> bool:
        if 0 <= sub_alpha <= 1:
            return True
        return False

    def _subanimation_is_complete(self, subanimation: BaseSubanimation, sub_alpha: float) -> bool:
        if sub_alpha == 1 and subanimation._has_started and isinstance(subanimation, LeafSubanimation):
            return True
        return False

    def flatten(self) -> None:
        for subanimation in self._subanimations:
            if isinstance(subanimation, SubanimationGroup):
                yield from subanimation.flatten()
            else:
                yield subanimation

    def insert(self, index: int, subanimation: BaseSubanimation) -> None:
        self._subanimations.insert(index, subanimation)

    def add(self, *subanimations: BaseSubanimation) -> None:
        for sub in subanimations:
            self._subanimations.append(sub)

    def get(self, index: int) -> BaseSubanimation:
        return self._subanimations[index]

    def set(self, index: int, subanimation: BaseSubanimation) -> None:
        self._subanimations[index] = subanimation

    def remove(self, subanimation: BaseSubanimation) -> None:
        self._subanimations.remove(subanimation)

    def get_run_time(self) -> float:
        total_run_time: float = 0
        subanimation_run_times: list[float] = []
        for subanimation in self._subanimations:
            subanimation_run_times.append(subanimation.get_run_time())
        if self._lag_ratio == 0:
            total_run_time = max(subanimation_run_times)
        else:
            total_run_time = subanimation_run_times[0]
            start_index: int = 1
            for i, curr_run_time in enumerate(subanimation_run_times[start_index:]):
                prev_run_time: float = subanimation_run_times[i - 1]
                curr_start: float = total_run_time - \
                    ((1 - self._lag_ratio) * prev_run_time)

                total_run_time = curr_start + curr_run_time
        return total_run_time

    def get_num_subanimations(self) -> int:
        total_num_subanimations: int = 0
        for subanimation in self._subanimations:
            total_num_subanimations += subanimation.get_num_subanimations()
        return total_num_subanimations

    def is_successive_group(self) -> bool:
        return self._lag_ratio == 1

    def has_one_subanimation(self) -> bool:
        return len(self._subanimations) == 1

    def contains_subanimations(self) -> bool:
        return self.get_num_subanimations() > 0

    def sub_in_successive_counterparts(self) -> SubanimationGroup:
        for i, subanimation in enumerate(self._subanimations):
            if isinstance(subanimation, LeafSubanimation):
                self._subanimations[i] = subanimation.create_successive_counterpart(
                )
            else:
                subanimation.sub_in_successive_counterparts()

    def create_successive_counterpart(self) -> SubanimationGroup:
        successive_subanimations: list = []
        for subanimation in self._subanimations:
            successive_subanimations += subanimation._create_successive_counterpart()
        return SubanimationGroup(*successive_subanimations, lag_ratio=1)

    def _create_successive_counterpart(self) -> list[BaseSubanimation]:
        successive_subanimations: list = []
        for subanimation in self._subanimations:
            successive_subanimations += subanimation._create_successive_counterpart()
        return successive_subanimations

    @property
    def lag_ratio(self) -> float:
        return self._lag_ratio

    @lag_ratio.setter
    def lag_ratio(self, new_lag_ratio: float) -> None:
        self._lag_ratio = new_lag_ratio
