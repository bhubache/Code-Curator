from __future__ import annotations

import difflib

from .custom_code import CustomCode


class CodeDiff:
    def __init__(self, source_obj: CustomCode, destination_obj: CustomCode) -> None:
        self._source_obj = source_obj
        self._destination_obj = destination_obj
        self._diff = self._create_diff()

    def __str__(self) -> str:
        return '\n'.join(self.difference)

    def __iter__(self) -> list:
        return self.difference.__iter__()

    def __len__(self) -> int:
        return len(self.difference)

    def __getitem__(self, index: int) -> str:
        return self.difference[index]

    def __setitem__(self, index: int, item: str) -> None:
        self.difference[index] = item

    @property
    def source(self):
        return self._source_obj

    @property
    def destination(self):
        return self._destination_obj

    @property
    def difference(self):
        return self._diff

    def line_unique_to_src_code(self, line: str) -> bool:
        return line.startswith('- ')

    def line_unique_to_dst_code(self, line: str) -> bool:
        return line.startswith('+ ')

    def line_common_to_both_codes(self, line: str) -> bool:
        return line.startswith('  ')

    def line_not_present_in_either_code(self, line: str) -> bool:
        return line.startswith('? ')

    def get_destination_line(self, line_index: int):
        return self._get_destination_line_attr(line_index=line_index, attr='line')

    def get_destination_line_index(self, line_index: int) -> int:
        return self._get_destination_line_attr(line_index=line_index, attr='index')

    def _get_destination_line_attr(self, line_index: int, attr: str) -> str | int:
        line_exclude_count = 0
        for i, line in enumerate(self):
            if self.line_not_present_in_either_code(line) or self.line_unique_to_src_code(line):
                line_exclude_count += 1
            elif i == line_index:
                if attr == 'index':
                    return i - line_exclude_count
                elif attr == 'line':
                    return self.destination[2][i - line_exclude_count]
                else:
                    raise RuntimeError(f'Unexpected attr: {attr}')
        return None

    def get_source_line(self, line_index: int):
        return self._get_source_line_attr(line_index=line_index, attr='line')

    def get_source_line_index(self, line_index: int) -> int:
        return self._get_source_line_attr(line_index=line_index, attr='index')

    def _get_source_line_attr(self, line_index: int, attr: str) -> str | int:
        line_exclude_count = 0
        for i, line in enumerate(self):
            if self.line_not_present_in_either_code(line) or self.line_unique_to_dst_code(line):
                line_exclude_count += 1
            elif i == line_index:
                if attr == 'index':
                    return i - line_exclude_count
                elif attr == 'line':
                    return self.source[2][i - line_exclude_count]
                else:
                    raise RuntimeError(f'Unexpected attr: {attr}')
        return None

    def line_was_added(self, line_index: int) -> bool:
        if line_index == 0 and self.line_unique_to_dst_code(self[line_index]):
            return True

        if self.line_unique_to_dst_code(self[line_index]) and not self.line_unique_to_src_code(self[line_index - 1]):
            return True

        return False

    def _get_diff_char_list(self, word: str) -> list[str]:
        diff_char_arr = []
        for i in range(0, len(word), 3):
            diff_char_arr.append(f'{word[i]}{word[i + 1]}{word[i + 2]}')
        return diff_char_arr

    def word_contains_added_char(self, word: str) -> bool:
        diff_chars = self._get_diff_char_list(word)

        for diff_str in diff_chars:
            if diff_str.startswith('+ '):
                return True
        return False

    def word_contains_removed_char(self, word):
        diff_chars = self._get_diff_char_list(word)

        for diff_str in diff_chars:
            if diff_str.startswith('- '):
                return True
        return False

    def get_sequence_similarity(self, seq_one: str, seq_two: str) -> float:
        return difflib.SequenceMatcher(None, seq_one, seq_two).ratio()

    def _create_diff(self) -> list[str]:
        diff = list(
            difflib.ndiff(
                self.source.code_string.splitlines(),
                self.destination.code_string.splitlines(),
            ),
        )

        # Remove lines that are not present in either code
        cleaned_diff = []
        for line in diff:
            if self.line_not_present_in_either_code(line):
                continue

            cleaned_diff.append(line)
        return cleaned_diff
