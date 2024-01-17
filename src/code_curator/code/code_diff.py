from __future__ import annotations

import difflib
from typing import TYPE_CHECKING

from manim import FadeIn
from manim import FadeOut
from manim import Mobject

if TYPE_CHECKING:
    from .curator_code import CuratorCode


class CodeDiff:
    def __init__(self, source_obj: CuratorCode, destination_obj: CuratorCode) -> None:
        self.source = source_obj
        self.destination = destination_obj

        self.diff_with_delta = list(
            difflib.ndiff(
                self.source.code_string.splitlines(),
                self.destination.code_string.splitlines(),
            ),
        )

        self.diff_without_delta = []
        for line in self.diff_with_delta:
            if self.line_not_present_in_either_code(line):
                continue

            self.diff_without_delta.append(line)

        self.matching_line_pairs: list[tuple[Mobject, Mobject]] = []
        self.added_lines: list[Mobject] = []
        self.removed_lines: list[Mobject] = []
        self.changed_line_pairs: list[LineDiffTokens] = []

        for source_line_index, original_line in enumerate(self.source.code_string.splitlines()):
            # TODO: Figure out how to handle empty lines
            if not original_line.strip():
                continue

            one_line_diff = list(difflib.ndiff([original_line], self.destination.code_string.splitlines()))
            if any(self.line_not_present_in_either_code(line) for line in one_line_diff):
                index = [i for i, line in enumerate(self.diff_without_delta) if line[2:] == original_line][0]

                self.changed_line_pairs.append(
                    LineDiffTokens(
                        source_line_string=original_line,
                        source_line_mobject=self.get_source_line(index),
                        destination_line_string=self.diff_without_delta[index + 1][2:],
                        destination_line_mobject=self.get_destination_line(index + 1),
                    ),
                )
            elif any(self.line_common_to_both_codes(line) for line in one_line_diff):
                index = [i for i, line in enumerate(self.diff_without_delta) if line[2:] == original_line][0]
                self.matching_line_pairs.append(
                    (
                        self.get_source_line(index),
                        self.get_destination_line(index),
                    ),
                )
            elif self.line_unique_to_src_code(one_line_diff[0]):
                self.removed_lines.append(self.source.get_line(source_line_index + 1))
            else:
                raise RuntimeError(f"Unexpected one line diff {one_line_diff}")

        for destination_line_index, destination_line in enumerate(self.destination.code_string.splitlines()):
            one_line_diff = list(difflib.ndiff([destination_line], self.source.code_string.splitlines()))
            if self.line_unique_to_src_code(one_line_diff[0]) and not self.line_not_present_in_either_code(
                one_line_diff[1],
            ):
                self.added_lines.append(self.destination.get_line(destination_line_index + 1))

    def __str__(self) -> str:
        return "\n".join(self.diff_without_delta)

    def __iter__(self) -> list:
        return self.diff_without_delta.__iter__()

    def __len__(self) -> int:
        return len(self.diff_without_delta)

    def __getitem__(self, index: int) -> str:
        return self.diff_without_delta[index]

    def __setitem__(self, index: int, item: str) -> None:
        self.diff_without_delta[index] = item

    def line_unique_to_src_code(self, line: str) -> bool:
        return line.startswith("- ")

    def line_unique_to_dst_code(self, line: str) -> bool:
        return line.startswith("+ ")

    def line_common_to_both_codes(self, line: str) -> bool:
        return line.startswith("  ")

    def line_not_present_in_either_code(self, line: str) -> bool:
        return line.startswith("? ")

    def get_destination_line(self, line_index: int):
        return self._get_destination_line_attr(line_index=line_index, attr="line")

    def get_destination_line_index(self, line_index: int) -> int:
        return self._get_destination_line_attr(line_index=line_index, attr="index")

    def _get_destination_line_attr(self, line_index: int, attr: str) -> str | int:
        line_exclude_count = 0
        for i, line in enumerate(self):
            if self.line_not_present_in_either_code(line) or self.line_unique_to_src_code(line):
                line_exclude_count += 1
            elif i == line_index:
                if attr == "index":
                    return i - line_exclude_count
                elif attr == "line":
                    return self.destination[2][i - line_exclude_count]
                else:
                    raise RuntimeError(f"Unexpected attr: {attr}")
        return None

    def get_source_line(self, line_index: int):
        return self._get_source_line_attr(line_index=line_index, attr="line")

    def get_source_line_index(self, line_index: int) -> int:
        return self._get_source_line_attr(line_index=line_index, attr="index")

    def _get_source_line_attr(self, line_index: int, attr: str) -> str | int:
        line_exclude_count = 0
        for i, line in enumerate(self):
            if self.line_not_present_in_either_code(line) or self.line_unique_to_dst_code(line):
                line_exclude_count += 1
            elif i == line_index:
                if attr == "index":
                    return i - line_exclude_count
                elif attr == "line":
                    return self.source[2][i - line_exclude_count]
                else:
                    raise RuntimeError(f"Unexpected attr: {attr}")
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
            diff_char_arr.append(f"{word[i]}{word[i + 1]}{word[i + 2]}")
        return diff_char_arr

    def word_contains_added_char(self, word: str) -> bool:
        diff_chars = self._get_diff_char_list(word)

        for diff_str in diff_chars:
            if diff_str.startswith("+ "):
                return True
        return False

    def word_contains_removed_char(self, word):
        diff_chars = self._get_diff_char_list(word)

        for diff_str in diff_chars:
            if diff_str.startswith("- "):
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


class LineDiffTokens:
    def __init__(
        self,
        source_line_string: str,
        source_line_mobject: Mobject,
        destination_line_string: str,
        destination_line_mobject: Mobject,
    ) -> None:
        self.source_line_string = source_line_string
        self.source_line_mobject = source_line_mobject
        self.destination_line_string = destination_line_string
        self.destination_line_mobject = destination_line_mobject

        self.char_diff = list(difflib.ndiff(self.source_line_string, self.destination_line_string))

        animations = []

        source_index: int = 0
        destination_index: int = 0

        for char in self.char_diff:
            if char.startswith(" "):
                animations.append(
                    self.source_line_mobject[source_index].animate.move_to(
                        self.destination_line_mobject[destination_index],
                    ),
                )
                source_index += 1
                destination_index += 1
            elif char.startswith("-"):
                animations.append(FadeOut(self.source_line_mobject[source_index]))
                source_index += 1
            elif char.startswith("+"):
                animations.append(FadeIn(self.destination_line_mobject[destination_index]))
                destination_index += 1

        self.animations = animations
