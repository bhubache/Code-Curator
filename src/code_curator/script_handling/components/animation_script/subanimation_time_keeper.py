from __future__ import annotations

import copy
from collections.abc import Sequence

from ...components.alignment_script.alignments.aligned_word import AlignedWord

# TODO: May need to make copies of these objects if they are to be reused!

class SubanimationTimeKeeper:
    """Stores timing information for all contiguous substrings of a subanimation.

    Example:
        curve_pointer: and   set    it   equal  to    p2.
                      [0.38, 0.21, 0.18, 0.33, 0.22, 0.47]
    """

    def __init__(self, text: str, words: Sequence[AlignedWord], time_until_start: float) -> None:
        self._check_input(text, words)
        self.text = text
        self.words = words
        self.word_timings = [word.duration for word in words]
        self.time_until_start = time_until_start

        self._original_text_copy = self.text
        self._original_words_copy = self.words.copy()
        self._original_word_timings = self.word_timings.copy()

    def __getitem__(self, item: str) -> float:
        try:
            return getattr(self, f'_total_{item}')
        except AttributeError:
            return getattr(self, f'total_{item}')

    def __setitem__(self, item: str, value: float) -> None:
        setattr(self, f'_total_{item}', value)

    def copy(self) -> SubanimationTimeKeeper:
        return copy.deepcopy(self)

    def _check_input(self, text: str, words: Sequence[AlignedWord]) -> None:
        if len(text.split()) != len(words):
            raise ValueError(f'Length of text does not match length of word_timings: {len(text.split())} != {len(words)}')

        for text_word, aligned_word in zip(text.split(), words):
            if text_word != aligned_word.text:
                raise ValueError('Aligned words are not matching up with text from yaml file!')

    @property
    def total_run_time(self) -> float:
        return sum(self.word_timings)

    def get_sequence_time(self, sequence: str, occurrence: int | None = None) -> float:
        assert len(self.text.split()) == len(self.words)
        # breakpoint()
        partition = self.partition(sequence=sequence, occurrence=occurrence)
        start_index = len(partition[0].split())
        stop_index = len(partition[0].split()) + len(partition[1].split())
        return sum(
            [word.duration for word in self.words[start_index:stop_index]]
        )

    def get_time_before_sequence(self, sequence: str, occurrence: int | None = None) -> float:
        pass

    # def partition(self, substring: str, occurrence: int | None = None) -> tuple[str, str, str]:
    #     return self.text.partition(substring)

    def partition(self, sequence: str, occurrence: int | None = None) -> float:
        """Return [start, stop) of ``sequence``."""
        if self.text.count(sequence) > 1 and occurrence is None:
            raise ValueError(
                f'There is more than one occurrence of ``sequence`` ``{sequence}`` in ``{self.text}``, yet an occurrence has not been specified. Please provide one.'
            )
        elif occurrence is None:
            occurrence = 1

        partition: tuple[str, str, str] = self.text.partition(sequence)
        for _ in range(occurrence - 1):
            partition = self._strip_elements_of_partition(partition)

            sub_partition = partition[2].partition(sequence)
            sub_partition = self._strip_elements_of_partition(sub_partition)

            partition = (
                ' '.join((partition[0], partition[1], sub_partition[0])),
                sub_partition[1],
                sub_partition[2]
            )

        return self._strip_elements_of_partition(partition)

    def _strip_elements_of_partition(self, partition: tuple[str, str, str]) -> tuple[str, str, str]:
        return tuple([s.strip() for s in partition])

    def reset(self) -> None:
        self.text = self._original_text_copy
        self.words = self._original_words_copy
        self.word_timings = self._original_word_timings
