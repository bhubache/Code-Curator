from .script_animation import ScriptAnimation
from ..alignment_script.alignments.aligned_script import AlignedScript

from typing import Iterable

class ScriptOrder:
    unique_id = 0
    def __init__(self, order_id: str = None, text: str = None):
        self._order_id = self._get_id(order_id)
        self._text = text.strip()
        self._num_words = len(self._text.split())

        self._animation_marker_start = '<a>'
        self._animation_marker_end = '</a>'

        self._script_animations = self._get_script_animations()

    def __str__(self):
        return '\n'.join([str(script_animation) for script_animation in self._script_animations])

    @property
    def order_id(self):
        return self._order_id

    @property
    def num_words(self):
        return self._num_words

    def apply_alignments(self, aligned_script: AlignedScript, word_count_start: int):
        for script_animation in self._script_animations:
            script_animation.apply_alignments(aligned_script.get_words_from_to(start=word_count_start, end=word_count_start + script_animation.num_words - 1))
            word_count_start += script_animation.num_words

    def get_animation_timings(self):
        timing_info = {}
        if len(self._script_animations) == 1:
            return self._script_animations[0].get_animation_timings()

        for i, script_animation in enumerate(self._script_animations):
            timing_info[i] = script_animation.get_animation_timings()
        # for script_animation in self._script_animations:
        #     timing_info[self.order_id] = script_animation.get_animation_timings()
        return timing_info

    def _get_script_animations(self):
        script_animations = []
        order_words = self._text.split()

        animation_index_start = 0
        for i, word in enumerate(order_words):
            if self._animation_marker_end in word:
                assert self._animation_marker_end in word, f'Error: {self._animation_marker_start} and {self._animation_marker_end} span more than one word in the script!!!'
                script_animations.append(
                    self._create_script_animation(start_index=animation_index_start, end_index=i, order_words=order_words)
                )
                animation_index_start = i
            elif i == len(order_words) - 1:
                script_animations.append(
                    self._create_script_animation(start_index=animation_index_start, end_index=i + 1, order_words=order_words)
                )
        return script_animations

    def _create_script_animation(self, start_index: int, end_index: int, order_words: Iterable[str]) -> ScriptAnimation:
        start_word = self._remove_animation_marker(order_words[start_index])
        return ScriptAnimation(
            text=f'{start_word} {" ".join(order_words[start_index + 1 : end_index])}'
        )
    
    def _remove_animation_marker(self, word: str) -> str:
        cleaned_word = word.replace(self._animation_marker_start, '')
        cleaned_word = cleaned_word.replace(self._animation_marker_end, '')
        return cleaned_word

    def _get_id(self, order_id):
        if order_id is not None: return order_id
        
        ScriptOrder.unique_id += 1
        return ScriptOrder.unique_id
        # unique_id = 1
        # def inner():
        #     if order_id is not None: return order_id

        #     return unique_id
        # unique_id += 1
        # return inner
