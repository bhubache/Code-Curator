from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING

from code_curator.animations.singly_linked_list.subanimations.base_subanimation import BaseSubanimation
from code_curator.custom_logging.custom_logger import CustomLogger
from manim import Animation

if TYPE_CHECKING:
    from code_curator.animations.singly_linked_list.data_structure_animator import DataStructureAnimator
    from manim import Scene
    from code_curator.data_structures.singly_linked_list import SinglyLinkedList
    from .subanimation_group import SubanimationGroup

__all__: list[str] = ['DataStructureAnimation']

logger = CustomLogger.getLogger(__name__)


def _update_animation(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.run_time = self._animator.get_run_time()
        self._subanimation_group = self._animator.get_subanimation_group()
        self._subanimation_group.init_run_time()

        return result
    return inner


class DataStructureAnimation(Animation):
    """Animation for all data structures."""

    def __init__(self, sll: SinglyLinkedList, data_structure_animator: DataStructureAnimator) -> None:
        """Initialize member variables.

        Args:
            sll: The data structure to be animated.
            data_structure_animator: The object controlling the animation.
        """
        super().__init__(sll, run_time=data_structure_animator.run_time)
        self._sll: SinglyLinkedList = sll
        self._animator: DataStructureAnimator = data_structure_animator
        # self._subanimation_group: SubanimationGroup = self._animator.get_subanimation_group()
        # self._subanimation_group = self._animator.animation_groups

        # self.run_time = self._animator.get_run_time()
        # self._subanimation_group = self._animator.get_subanimation_group()
        # self._subanimation_group.init_run_time()

    def begin(self) -> None:
        """Set up the animation."""
        self.run_time = self._animator.run_time
        # self._subanimation_group = self._animator.get_subanimation_group()
        # self._subanimation_group.init_run_time()
        super().begin()
    
    def interpolate_mobject(self, alpha: float) -> None:
        """Create the animation.

        Args:
            alpha: The progress of the animation ranging from [0, 1].
        """
        self._animator.interpolate(alpha)

    def clean_up_from_scene(self, scene: Scene) -> None:
        """Clean up the animation.

        Args:
            scene: The scene in which the animation is taking place.
        """
        self._animator.clean_up_from_scene(scene)
        # self._animator.clean_up_mobject()
        super().clean_up_from_scene(scene)

    # @_update_animation
    def insert_subanimation(self, index: int, subanimation: BaseSubanimation) -> None:
        """Insert a subanimation into the animation.

        Args:
            index: Index at which to insert the subanimation.
            subanimation: The subanimation to insert.
        """
        self._subanimation_group.insert(index, subanimation)

    # @_update_animation
    def remove_subanimation(self, index: int) -> None:
        """Remove a subanimation from the animation.

        Args:
            index: Index at which the subanimation should be removed.
        """
        self._subanimation_group.remove(self._subanimation_group.get(index))

    def set_timing(self, subanimation_identifier: str, run_time: float) -> None:
        """Set the timing of a subanimation."""
        success = self._subanimation_group.set_timing(
            identifier=subanimation_identifier,
            run_time=run_time,
        )
        if not success:
            raise LookupError(f'Unable to find subanimation {subanimation_identifier}')

    def pad_with_wait(self, subanimation_identifier: str, run_time: float) -> None:
        success = self._subanimation_group.pad_with_wait(
            identifier=subanimation_identifier,
            run_time=run_time,
        )
        if not success:
            raise LookupError(f'Unable to find subanimation {subanimation_identifier}')
        print(self._subanimation_group)
