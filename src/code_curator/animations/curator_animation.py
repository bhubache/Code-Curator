from __future__ import annotations

from typing import TYPE_CHECKING

from manim import Animation
from manim import Wait

from code_curator.custom_logging.custom_logger import CustomLogger


logger = CustomLogger.getLogger(__name__)


if TYPE_CHECKING:
    from manim import Mobject


class CuratorAnimation(Animation):
    _owner = None

    def __init__(
        self,
        *mobjects: Mobject,
        run_time: float | None = None,
        **kwargs,
    ) -> None:
        self.remaining_time = None
        run_time = self._check_run_time(
            run_time=run_time,
            owner=self.__class__._owner,
        )
        super().__init__(*mobjects, run_time=run_time, **kwargs)

    def _check_run_time(self, *, run_time: float, owner) -> float:
        available_time: float = owner.animation_name_timing_map[owner.func_name]

        if run_time is None:
            run_time = min(available_time, 1.0)

        if run_time > available_time:
            err_msg = (
                f"{owner.func_name} only has {available_time} second(s) of available"
                f" time. Attempted: {run_time} second(s)."
            )
            if self._is_wait_animation():
                notification_msg = (
                    "However, because it is a Wait animation, this run_time was"
                    " probably set internally by manim and so I am going to assume it"
                    " is ok to use the available time instead. Be careful that this is"
                    " not an animation you actually expect to last"
                    f" {run_time} second(s)"
                )
                logger.info(f"{err_msg} {notification_msg}")
                run_time = available_time
            else:
                raise ValueError(err_msg)

        self.remaining_time = available_time - run_time

        return run_time

    def _is_wait_animation(self) -> bool:
        return Wait in self.__class__.__mro__
