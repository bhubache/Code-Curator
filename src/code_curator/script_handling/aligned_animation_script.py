from __future__ import annotations

import copy
from collections.abc import Sequence

from .components.alignment_script.alignments.aligned_script import AlignedScript
from .components.animation_script.animation_leaf import AnimationLeaf
from .components.animation_script.composite_animation_script import CompositeAnimationScript


class AlignedAnimationScript:
    def __init__(self, aligned_script: AlignedScript, animation_script: CompositeAnimationScript):
        self._aligned_script:   AlignedScript = aligned_script
        self._animation_script: CompositeAnimationScript = animation_script
        self.run_time: float = aligned_script.get_full_duration()

        for stream in animation_script.values():
            stream.apply_alignments(-1, -1, self._aligned_script)
            entries_without_waits = []
            for entry in stream.entries:
                if entry["name"] != "-wait-":
                    entries_without_waits.append(entry)
            stream.entries = entries_without_waits

    def get_scenes(self) -> list[CompositeAnimationScript | AnimationLeaf]:
        return self._animation_script.children

    @property
    def stream_names(self) -> Sequence[str]:
        return self._animation_script.keys()