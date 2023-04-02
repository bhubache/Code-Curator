from __future__ import annotations

from .base_subanimation import BaseSubanimation
from data_structures.singly_linked_list import singly_linked_list

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)


class LeafSubanimation(BaseSubanimation):
    def __init__(self, sll):
        super().__init__()
        self._sll: singly_linked_list.SinglyLinkedList = sll

    def __str__(self) -> str:
        return self.__class__.__name__

    def _to_str_helper(self, start_time: float, end_time: float, recursion_level: int) -> str:
        return f'{"  " * (recursion_level)}{self.__class__.__name__}: {start_time}-{end_time}'

    def __len__(self):
        return 1

    def begin(self):
        pass

    def interpolate(self, alpha: float):
        pass

    def clean_up_from_animation(self):
        self._sll.save_state()

    def clean_up_from_scene(self, scene):
        pass

    def create_successive_counterpart(self) -> BaseSubanimation:
        pass

    def _create_successive_counterpart(self):
        return [self.create_successive_counterpart()]

    def is_successive_group(self) -> bool:
        return True

    def has_one_subanimation(self) -> bool:
        return True

    def get_num_subanimations(self) -> int:
        return 1
