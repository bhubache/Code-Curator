from __future__ import annotations

from .base_subanimation import BaseSubanimation
from data_structures.singly_linked_list import singly_linked_list

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

# NOTE: Put subanimations for SLL at the beginning of a group

class LeafSubanimation(BaseSubanimation):
    def __init__(self, sll, animates_sll: bool = False):
        super().__init__(animates_sll=animates_sll)
        self._sll: singly_linked_list.SinglyLinkedList = sll
        # self._sll: singly_linked_list.SinglyLinkedList = sll
        # self._animates_sll: bool = animates_sll
        # self._unique_id: str = f'{self._sll.__class__.__name__}_{self.__class__.__name__}'
        # self._final_sll = singly_linked_list.SinglyLinkedList.create_sll(self._sll)
        # self._sll_post_subanimation_group = None
        # self._custom_sll_saved_state = self._sll.copy()

    def __str__(self) -> str:
        return self.__class__.__name__

    def _to_str_helper(self, start_time: float, end_time: float, recursion_level: int) -> str:
        return f'{"  " * (recursion_level)}{self.__class__.__name__}: {start_time}-{end_time}'

    def __len__(self):
        return 1

    def begin(self):
        pass

    def get_num_subanimations(self) -> int:
        return len(self)

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

    def get_sll(self):
        return self._sll

    def is_successive_group(self) -> bool:
        return True

    def has_one_subanimation(self) -> bool:
        return True

    @property
    def sll_post_subanimation_group(self):
        return self._sll_post_subanimation_group

    @sll_post_subanimation_group.setter
    def sll_post_subanimation_group(self, sll) -> None:
        self._sll_post_subanimation_group = sll
