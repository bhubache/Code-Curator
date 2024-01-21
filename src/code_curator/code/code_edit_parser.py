from __future__ import annotations

import itertools as it
import re

REMOVED_LINE_PATTERN = "<<<<<REMOVE>>>>>"
ADDED_LINE_PATTERN = "<<<<<ADD>>>>>"
EDITED_STR_PATTERN = r"<<<<<EDIT\((.*?), (.*?)\)>>>>>"


def clean_code_string(text: str) -> str:
    text = re.sub(rf"{REMOVED_LINE_PATTERN}.*\n?", "", text)
    text = text.replace(ADDED_LINE_PATTERN, "")
    while match := re.search(EDITED_STR_PATTERN, text):
        text = text.replace(match.group(), match.group(2))

    return text


def line_changed(line: str) -> bool:
    return line_is_removed(line) or line_is_added(line) or line_is_edited(line)


def line_is_removed(line: str) -> bool:
    return bool(re.findall(REMOVED_LINE_PATTERN, line))


def line_is_added(line: str) -> bool:
    return bool(re.findall(ADDED_LINE_PATTERN, line))


def line_is_edited(line: str) -> bool:
    return bool(re.findall(EDITED_STR_PATTERN, line))


def pairwise_edited_line_bounds(line: str):
    source_start = 0
    target_start = 0

    edit_pairs: list[tuple[str | None, str | None]] = re.findall(EDITED_STR_PATTERN, line) + [(None, None)]

    substring_pairs: list[tuple[str, str]] = list(it.pairwise(re.split(EDITED_STR_PATTERN, line)))
    substring_pairs.append((substring_pairs[-1][-1], "DUMMY TEXT"))

    substring_pair_index = 0
    while substring_pair_index < len(substring_pairs):
        substring_one, substring_two = substring_pairs[substring_pair_index]
        if substring_one == edit_pairs[0][0] and substring_two == edit_pairs[0][1]:
            yield source_start, source_start + len(substring_one), target_start, target_start + len(substring_two), True

            source_start += len(substring_one)
            target_start += len(substring_two)

            edit_pairs.pop(0)

            substring_pair_index += 2
        else:
            yield source_start, source_start + len(substring_one), target_start, target_start + len(
                substring_one,
            ), False

            source_start += len(substring_one)
            target_start += len(substring_one)

            substring_pair_index += 1
