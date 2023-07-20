from __future__ import annotations

from code_curator.custom_logging.custom_logger import CustomLogger
from code_curator.animations.singly_linked_list.subanimations.leaf_subanimation import LeafSubanimation

logger = CustomLogger.getLogger(__name__)


class WaitSubanimation(LeafSubanimation):
    def __init__(self, sll, run_time: int = 1):
        super().__init__(sll=sll, run_time=run_time)

    def begin(self) -> None:
        pass

    def interpolate(self, alpha: float) -> None:
        pass

    def clean_up_from_animation(self) -> None:
        pass

    def create_successive_counterpart(self) -> LeafSubanimation:
        return WaitSubanimation(sll=self._sll, run_time=self._run_time)
