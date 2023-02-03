from .script_scene import ScriptScene
from ..alignment_script.alignments.aligned_script import AlignedScript

from typing import Iterable

class AlignedAnimationScript:
    def __init__(self, scenes: Iterable[ScriptScene]):
        self._scenes: Iterable[ScriptScene] = scenes

    def __str__(self):
        output = ''
        for scene in self._scenes:
            output += f'\n\n{scene}'
        return output

    @property
    def scenes(self) -> Iterable[ScriptScene]:
        return self._scenes

    def apply_alignments(self, aligned_script: AlignedScript):
        word_count_start = 1
        for scene in self._scenes:
            scene.apply_alignments(aligned_script.get_words_from_to(start=word_count_start, end=word_count_start + scene.num_words - 1), word_count_start=word_count_start)
            word_count_start += scene.num_words

    def get_animation_timings(self) -> dict:
        timing_info = {}
        for scene in self._scenes:
            timing_info[scene.scene_id] = scene.get_animation_timings()
        return timing_info

    def print_animation_timings(self):
        import json
        print(json.dumps(self.get_animation_timings(), indent=4, default=str, ensure_ascii=False))
    