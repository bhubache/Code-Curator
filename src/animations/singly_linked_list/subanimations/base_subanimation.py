from __future__ import annotations
from abc import ABC, abstractmethod
import copy

from data_structures.singly_linked_list import singly_linked_list

from custom_logging.custom_logger import CustomLogger
logger = CustomLogger.getLogger(__name__)

class BaseSubanimation(ABC):
    def __init__(self, sll):
        self._sll: singly_linked_list.SinglyLinkedList = sll
        self._unique_id: str = f'{self._sll.__class__.__name__}_{self.__class__.__name__}'
        self._final_sll = singly_linked_list.SinglyLinkedList.create_sll(self._sll)
        self._sll_post_subanimation_group = None

    @property
    def sll_post_subanimation_group(self):
        return self._sll_post_subanimation_group

    @sll_post_subanimation_group.setter
    def sll_post_subanimation_group(self, sll) -> None:
        self._sll_post_subanimation_group = sll

    # def copy(self) -> BaseSubanimation:
    #     return copy.deepcopy(self)
    
    def begin(self):
        self._sll.restore()

    @abstractmethod
    def interpolate(self, alpha: float):
        pass

    def clean_up_from_animation(self):
        self._sll.save_state()

    def clean_up_from_scene(self, scene):
        pass

    # def _save_sll_state(self):
    #     return self._sll.save_state()
    #     return self._sll.save_state(self._unique_id)

    # def _restore_sll(self):
    #     return self._sll.restore()
    #     return self._sll.restore(self._unique_id)