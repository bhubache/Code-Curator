from __future__ import annotations

from animations.singly_linked_list import data_structure_animator as ds_animator
from custom_logging.custom_logger import CustomLogger
from data_structures import singly_linked_list as sll_m
from manim import Animation

from .subanimation_group import SubanimationGroup
logger = CustomLogger.getLogger(__name__)


class DataStructureAnimation(Animation):
    def __init__(self, sll, data_structure_animator) -> None:
        super().__init__(sll, run_time=data_structure_animator.get_run_time())
        self._sll: sll_m.SinglyLinkedList = sll
        self._animator: ds_animator.DataStructureAnimator = data_structure_animator
        self._subanimation_group: SubanimationGroup = self._animator.get_subanimation_group()

    def begin(self) -> None:
        self._subanimation_group.init_run_time()
        super().begin()

    def interpolate_mobject(self, alpha) -> None:
        self._subanimation_group.interpolate(alpha)

    def clean_up_from_scene(self, scene) -> None:
        self._subanimation_group.clean_up_from_scene(scene)
        self._animator.clean_up_mobject()
        return super().clean_up_from_scene(scene)
    
    def add_animation(self, index: int, animation) -> None:
        self._subanimation_group.insert(index, animation)

    def remove_animation(self, index: int) -> None:
        self._subanimation_group.remove(self._subanimation_group.get(index))
