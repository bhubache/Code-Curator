from __future__ import annotations

from typing import TYPE_CHECKING

from animations.singly_linked_list.subanimations.base_subanimation import BaseSubanimation
from custom_logging.custom_logger import CustomLogger
from manim import Animation

if TYPE_CHECKING:
    from data_structures.singly_linked_list import SinglyLinkedList
    from animations.singly_linked_list.data_structure_animator import DataStructureAnimator

from .subanimation_group import SubanimationGroup
logger = CustomLogger.getLogger(__name__)


class DataStructureAnimation(Animation):
    def __init__(self, sll: SinglyLinkedList, data_structure_animator: DataStructureAnimator) -> None:
        super().__init__(sll, run_time=data_structure_animator.get_run_time())
        self._sll: SinglyLinkedList = sll
        self._animator: DataStructureAnimator = data_structure_animator
        self._subanimation_group: SubanimationGroup = self._animator.get_subanimation_group()

    def begin(self) -> None:
        self.run_time = self._animator.get_run_time()
        self._subanimation_group = self._animator.get_subanimation_group()
        self._subanimation_group.init_run_time()
        super().begin()

    def interpolate_mobject(self, alpha) -> None:
        self._subanimation_group.interpolate(alpha)

    def clean_up_from_scene(self, scene) -> None:
        self._subanimation_group.clean_up_from_scene(scene)
        self._animator.clean_up_mobject()
        return super().clean_up_from_scene(scene)

    def insert_subanimation(self, index: int, subanimation: BaseSubanimation) -> None:
        self._subanimation_group.insert(index, subanimation)

    def remove_subanimation(self, index: int) -> None:
        self._subanimation_group.remove(self._subanimation_group.get(index))
