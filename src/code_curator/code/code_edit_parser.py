from __future__ import annotations

import itertools as it
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from code_curator.code.curator_code import CuratorCode


REMOVED_LINE_PATTERN = "<<<<<REMOVE>(.)</REMOVE>>>>>"
ADDED_LINE_PATTERN = "<<<<<ADD>(.)</ADD>>>>>"


def decode_string(text: str) -> str:
    while match := re.search(REMOVED_LINE_PATTERN, text):
        text = text.replace(match.group(), "")

    while match := re.search(ADDED_LINE_PATTERN, text):
        text = text.replace(match.group(), match.group(1))

    return text


def partitioned_chars(original_code: CuratorCode, target_code: CuratorCode):
    original_code_chars = list(it.chain.from_iterable(original_code.code_paragraph))
    target_code_chars = list(it.chain.from_iterable(target_code.code_paragraph))

    matching_char_pairs = []
    added_chars = []
    removed_chars = []

    encoded_str_no_newlines = target_code.encoded_string.replace("\n", "")
    added_char_matches = (match for match in re.finditer(ADDED_LINE_PATTERN, encoded_str_no_newlines))
    removed_char_matches = (match for match in re.finditer(REMOVED_LINE_PATTERN, encoded_str_no_newlines))

    class DefaultMatch:
        def start(self):
            ...

        def end(self):
            ...

    char_index = 0
    original_char_index = 0
    target_char_index = 0
    next_added_match = next(added_char_matches, DefaultMatch())
    next_removed_match = next(removed_char_matches, DefaultMatch())
    while char_index < len(encoded_str_no_newlines):
        if char_index == next_added_match.start():
            added_chars.append(target_code_chars[target_char_index])
            char_index = next_added_match.end()
            next_added_match = next(added_char_matches, DefaultMatch())
            target_char_index += 1
        elif char_index == next_removed_match.start():
            removed_chars.append(original_code_chars[original_char_index])
            char_index = next_removed_match.end()
            next_removed_match = next(removed_char_matches, DefaultMatch())
            original_char_index += 1
        else:
            matching_char_pairs.append(
                (
                    original_code_chars[original_char_index],
                    target_code_chars[target_char_index],
                ),
            )
            original_char_index += 1
            target_char_index += 1
            char_index += 1

    return matching_char_pairs, added_chars, removed_chars
