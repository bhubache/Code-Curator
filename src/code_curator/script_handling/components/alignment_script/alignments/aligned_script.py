from __future__ import annotations

from collections.abc import Iterable

from .aligned_word import AlignedWord

SCRIPT = "Now, let's analyze the constraints. that is not the case, so the constraint skipping stuff a lot of words. Here, we have a linked list with pointer p situated at the head and we're going to remove the third node."


class AlignedScript:
    def __init__(self, text_data: dict[int, str] | dict[int, AlignedWord]):
        # self._words: dict[AlignedWord] = self._strs_to_words(
            # text_data,
        # ) if not self._dict_contains_aligned_words(text_data) else text_data
        self._words = {}

        time: float = 0.0
        delta = 0.25

        for index, word in enumerate(SCRIPT.split()):
            self._words[index + 1] = AlignedWord(
                {
                    "start": time,
                    "end": time + delta,
                    "text": word
                }
            )
            time += delta

    def __str__(self) -> str:
        return '\n'.join(f'{word_num} -> {word}' for word_num, word in self._words.items())

    def get_word(self, word_number: int) -> AlignedWord:
        return self._words[word_number]

    def get_word_start(self, word_number: int) -> float:
        return self.get_word(word_number=word_number).start

    def get_word_end(self, word_number: int) -> float:
        return self.get_word(word_number=word_number).end

    def get_word_text(self, word_number: int) -> str:
        return self.get_word(word_number=word_number).text

    def get_word_duration(self, word_number: int) -> float:
        return self.get_word(word_number=word_number).duration

    def get_full_duration(self) -> float:
        index: int = 0
        first: int = 0
        last:  int = 0
        for key in self._words:
            if index == 0:
                first = key
            if index == len(self._words) - 1:
                last = key
            index += 1
        return self.get_word_duration_from_to(first, last)

    # def get_words_from_to(self, start: int, end: int) -> AlignedScript:
    #     ''' Inclusive bounds'''
    #     sub_dict = {}
    #     for word_num in range(start, end + 1):
    #         sub_dict[word_num] = self.get_word(word_num)
    #     return AlignedScript(text_data=sub_dict)

    def get_words_from_to(self, start: int, end: int) -> AlignedScript:
        ''' Exclusive bounds'''
        try:
            sub_dict = {}
            new_index = 1
            for word_num in range(start, end):
                sub_dict[new_index] = self.get_word(word_num)
                new_index += 1
            return AlignedScript(text_data=sub_dict)
        except Exception:
            print('keys available')
            print(self._words.keys())
            print(self._words.values())
            raise

    def get_word_duration_from_to(self, start: int, end: int) -> float:
        return round(self.get_word_end(end) - self.get_word_start(start), 2)

    def get_occurrences(self, text: str) -> Iterable[AlignedWord]:
        pass

    def _dict_contains_aligned_words(self, d: dict) -> bool:
        for value in d.values():
            if isinstance(value, AlignedWord):
                return True
        return False

    def _strs_to_words(self, all_text_data: dict) -> dict[AlignedWord]:
        all_words_data = {}
        for word_num, text_data in all_text_data.items():
            if not isinstance(word_num, int):
                continue
            all_words_data[word_num] = AlignedWord(text_data)
        return all_words_data
