import re

from .script_order import ScriptOrder
from ..alignment_script.alignments.aligned_script import AlignedScript

from typing import Iterable

class ScriptSection:
    section_id = 0
    def __init__(self, section_id: str, text: str):
        self._section_id = self._get_id(section_id)
        self._text = text.strip()
        self._orders = self._get_script_orders()
        self._num_words = len(self._text.split())

    def __str__(self):
        return '\n'.join([str(order) for order in self._orders])

    @property
    def section_id(self):
        return self._section_id

    @property
    def text(self):
        return self._text

    @property
    def num_words(self):
        return self._num_words

    def get_order(self, order_id: str) -> ScriptOrder:
        for order in self._orders:
            if order.order_id == order_id: return order
        return None

    def apply_alignments(self, aligned_script: AlignedScript, word_count_start: int):
        for order in self._orders:
            # order.apply_alignments(aligned_script.get_words_from_to(start=word_count_start, end=order.num_words))
            order.apply_alignments(aligned_script.get_words_from_to(start=word_count_start, end=word_count_start + order.num_words - 1), word_count_start=word_count_start)
            word_count_start += order.num_words

    def get_animation_timings(self):
        timing_info = {}
        if len(self._orders) == 1:
            return self._orders[0].get_animation_timings()

        for i, order in enumerate(self._orders):
            timing_info[order.order_id] = order.get_animation_timings()
        return timing_info

    def _get_script_orders(self) -> Iterable[ScriptOrder]:
        orders = []
        start_order_index = 0
        section_words = self._text.split()
        for i, word in enumerate(section_words):
            if self._word_has_explicit_order_start(word) and self._word_has_explicit_order_end(word):
                # <during>not</during> case in constraints analysis
                orders.append(ScriptOrder(text=' '.join(section_words[start_order_index : i])))
                orders.append(ScriptOrder(order_id=self._get_word_order(word), text=self._remove_order_marking(word)))
                start_order_index = i + 1
            elif self._word_has_explicit_order_start(word):
                word_order = self._get_word_order(word)
                orders.append(ScriptOrder(text=' '.join(section_words[start_order_index : i])))
                start_order_index = i
            elif self._word_has_explicit_order_end(word):
                word_order = self._get_word_order(word)
                start_word = self._remove_order_marking(section_words[start_order_index])
                middle_words = ' '.join(section_words[start_order_index + 1 : i])
                end_word = self._remove_order_marking(section_words[i])
                order_text = f'{start_word} {middle_words} {end_word}'
                orders.append(ScriptOrder(order_id=self._get_word_order(section_words[start_order_index]), text=order_text))
                start_order_index = i + 1
            elif i == len(section_words) - 1:
                orders.append(
                    ScriptOrder(text=' '.join(section_words[start_order_index:]))
                )
        return orders

    def _word_has_explicit_order_start(self, word: str):
        return '<pre>' in word or '<during>' in word or '<post>' in word

    def _word_has_explicit_order_end(self, word: str):
        return '</pre>' in word or '</during>' in word or '</post>' in word

    def _get_word_order(self, word: str):
        # If word is something like <during>not</during>
        double_marker_match = re.search(pattern=fr'>(.*)<', string=word, flags=re.DOTALL)
        if double_marker_match is not None:
            open_bracket_index = word.index('<')
            close_bracket_index = word.index('>')
            return word[open_bracket_index + 1 : close_bracket_index]
            # return double_marker_match.group(1).strip()
        # return f"<{re.search(pattern=fr'<(.*)>', string=word, flags=re.DOTALL).group(1).strip()}>"
        return f"{re.search(pattern=fr'<(.*)>', string=word, flags=re.DOTALL).group(1).strip()}"

    def _remove_order_marking(self, word: str):
        double_marker_match = re.search(pattern=fr'>(.*)<', string=word, flags=re.DOTALL)
        if double_marker_match is not None:
            return double_marker_match.group(1).strip()
        cleaned_word = None
        if self._word_has_explicit_order_start(word):
            cleaned_word = word.replace(self._get_word_order(word), '')
        elif self._word_has_explicit_order_end(word):
            cleaned_word = word.replace(self._get_word_order(word), '')

        if cleaned_word is None:
            raise RuntimeError('Word passed in to _remove_order_marking doesn\'t have markings to remove')
        return cleaned_word

    def _get_id(self, section_id):
        if section_id is not None: return section_id
        
        ScriptSection.unique_id += 1
        return ScriptSection.unique_id
