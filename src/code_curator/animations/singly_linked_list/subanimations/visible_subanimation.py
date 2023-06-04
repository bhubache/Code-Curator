from __future__ import annotations

from custom_logging.custom_logger import CustomLogger

from .base_subanimation import BaseSubanimation
logger = CustomLogger.getLogger(__name__)


class VisibleSubanimation(BaseSubanimation):
    # saved_states = {}
    # restored_states = {}

    def __init__(self, sll):
        super().__init__(sll)

    # def _save_states(self, *mobjects) -> None:
    #     for mobject in mobjects:
    #         if mobject not in VisibleSubanimation.saved_states:
    #             # VisibleSubanimation.saved_states[mobject] = mobject.save_state()
    #             VisibleSubanimation.saved_states[mobject] = mobject.copy()

    # def _restore_states(self) -> None:
    #     for curr_mob, change_to_mob in VisibleSubanimation.saved_states.items():
    #         if not isinstance(curr_mob, singly_linked_list.SinglyLinkedList):
    #             logger.info(f'Restoring {curr_mob} from class {self.__class__.__name__} {id(curr_mob)} to {id(change_to_mob)}')
    #             # mobject.restore()
    #             curr_mob.become(change_to_mob)
    #     if len(VisibleSubanimation.saved_states) > 0:
    #         VisibleSubanimation.restored_states.update(VisibleSubanimation.saved_states)
    #     VisibleSubanimation.saved_states = {}

    # def begin(self):
    #     self._restore_states()
    #     logger.info(id(self._sll))
    #     # self._rebind_restored_states()
    #     logger.info(id(self._sll))
