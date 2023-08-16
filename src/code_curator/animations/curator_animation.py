from __future__ import annotations

from typing import TYPE_CHECKING

from manim import Animation


if TYPE_CHECKING:
    from manim import Mobject


class CuratorAnimation(Animation):
    _owner = None

    def __init__(self, *mobjects: Mobject, run_time: float | None = None, **kwargs) -> None:
        self.remaining_time = None
        run_time = self._check_run_time(
            run_time=run_time,
            owner=self.__class__._owner,
        )
        super().__init__(*mobjects, run_time=run_time, **kwargs)

    def _check_run_time(self, *, run_time: float, owner) -> float:
        # 1. Find leaf node from owner.namespace_path
        # 2. Check that run_time <= audio_duration
        # 3. Make owner._subsequent_wait_animation_run_time or some similar variable for audio_duration - run_time
        # 4. Use ast to yield a Wait animation after current animation with remaining time
        available_time = owner.aligned_animation_script_owner.get_child(owner.func_name).audio_duration
        if run_time is None:
            run_time = min(available_time, 1.0)

        if run_time > available_time:
            raise ValueError(
                f'{owner.func_name} only has {available_time} second(s) of available time. Attempted: {run_time} second(s)'
            )

        self.remaining_time = available_time - run_time

        return run_time
