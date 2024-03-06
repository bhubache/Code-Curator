from __future__ import annotations

from manim import AnimationGroup


class CuratorAnimationGroup(AnimationGroup):
    """AnimationGroup for ``CuratorAnimation``."""


class CuratorSuccession(CuratorAnimationGroup):
    """Succession for ``CuratorAnimation``."""

    def __init__(self, *animations, lag_ratio: float = 1, **kwargs) -> None:
        super().__init__(*animations, lag_ratio=lag_ratio, **kwargs)
