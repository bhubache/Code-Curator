from __future__ import annotations
from abc import ABC, abstractmethod
import copy

from data_structures.singly_linked_list import singly_linked_list

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

# NOTE: Put subanimations for SLL at the beginning of a group

class BaseSubanimation(ABC):
    def __init__(self, animates_sll: bool = False, run_time: float = 1):
        # self._sll: singly_linked_list.SinglyLinkedList = sll
        self._animates_sll: bool = animates_sll
        self._run_time: float = run_time
        # self._unique_id: str = f'{self._sll.__class__.__name__}_{self.__class__.__name__}'
        # self._final_sll = singly_linked_list.SinglyLinkedList.create_sll(self._sll)
        self._sll_post_subanimation_group = None
        # self._custom_sll_saved_state = self._sll.copy()

        self._visited: bool = False
        self._has_started: bool = False

    def __len__(self):
        return 1

    def get_run_time(self) -> float:
        return self._run_time

    def _build_subanimations_with_timings(self) -> float:
        pass

        # self._sll.save_state()

    # def create_successive_copy_counterpart(self, subanimation_cls, )

    def copy(self) -> BaseSubanimation:
        return copy.deepcopy(self)

    def begin(self):
        pass
        # self._sll.become(self._custom_sll_saved_state)
        # self._sll.restore()

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

    # def assign_forecasted_mobjects(self)

    @property
    def sll_post_subanimation_group(self):
        return self._sll_post_subanimation_group

    @sll_post_subanimation_group.setter
    def sll_post_subanimation_group(self, sll) -> None:
        self._sll_post_subanimation_group = sll

    # def _save_sll_state(self):
    #     return self._sll.save_state()
    #     return self._sll.save_state(self._unique_id)

    # def _restore_sll(self):
    #     return self._sll.restore()
    #     return self._sll.restore(self._unique_id)
