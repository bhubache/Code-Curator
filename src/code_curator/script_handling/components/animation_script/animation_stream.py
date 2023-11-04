from __future__ import annotations

from ..alignment_script.alignments.aligned_script import AlignedScript


class AnimationStream:
    def __init__(self, name: str, **kwargs) -> None:
        self.name = name
        self.entries = []
        self.is_overriding_start: bool = kwargs.get("is_overriding_start", False)
        self.is_overriding_end: bool = kwargs.get("is_overriding_end", False)
        self.start_time: float = 0.0
        self.end_time: float = 0.0

    def append(
        self,
        text: str,
        is_overriding_start: bool = False,
        is_overriding_end: bool = False,
        name: str = "-wait-",
    ) -> None:
        # if name == '-wait-':
        #     return

        self.entries.append(
            {
                "text": text,
                "is_overriding_start": is_overriding_start,
                "is_overriding_end": is_overriding_end,
                "name": name,
            }
        )

    # def front_is_

    def apply_alignments(self, start, end, aligned_script: AlignedScript):
        word_count: int = 1
        for entry in self.entries:
            entry["start_time"] = aligned_script.get_word_start(word_count)
            word_count += len(entry["text"].split())
