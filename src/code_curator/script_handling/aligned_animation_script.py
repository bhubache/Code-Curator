from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Sequence
    from .components.alignment_script.alignments.aligned_script import AlignedScript
    from .components.animation_script.animation_leaf import AnimationLeaf
    from .components.animation_script.composite_animation_script import CompositeAnimationScript


class AlignedAnimationScript:
    def __init__(self, aligned_script: AlignedScript, animation_script: CompositeAnimationScript):
        self._aligned_script: AlignedScript = aligned_script
        self._animation_script: CompositeAnimationScript = animation_script

        for stream in animation_script.values():
            stream.apply_alignments(-1, -1, self._aligned_script)
            entries_without_waits = []
            for entry in stream.entries:
                if entry["name"] != "-wait-":
                    entries_without_waits.append(entry)

            stream.entries = entries_without_waits

        start_time = 0.0
        for entry in self.entries:
            if entry.get("start_here", False):
                start_time = entry["start_time"]
                self.run_time = self._aligned_script.get_full_duration() - start_time

        for index, _ in enumerate(self.entries):
            self.entries[index]["start_time"] -= start_time

    @property
    def entries(self):
        return self._animation_script["Video"].entries

    @property
    def stream_names(self) -> Sequence[str]:
        return self._animation_script.keys()

    def get_scenes(self) -> list[CompositeAnimationScript | AnimationLeaf]:
        return self._animation_script.children
