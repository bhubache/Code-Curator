from __future__ import annotations

import itertools as it
import logging
import re
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from code_curator.code.curator_code import CuratorCode


TEXT_REMOVE_START_MARKER = "<R>"
TEXT_REMOVE_END_MARKER = "</R>"

TEXT_ADD_START_MARKER = "<A>"
TEXT_ADD_END_MARKER = "</A>"


REMOVED_LINE_PATTERN = f"{TEXT_REMOVE_START_MARKER}(.|\n){TEXT_REMOVE_END_MARKER}"
ADDED_LINE_PATTERN = f"{TEXT_ADD_START_MARKER}(.|\n){TEXT_ADD_END_MARKER}"


def decode_string(text: str) -> str:
    while match := re.search(REMOVED_LINE_PATTERN, text):
        text = text.replace(match.group(), "")

    while match := re.search(ADDED_LINE_PATTERN, text):
        text = text.replace(match.group(), match.group(1))

    return text


def partitioned_chars(original_code: CuratorCode, target_code: CuratorCode):
    # Description of algorithm:
    #
    # Goal
    #     Return three lists:
    #     - matching_char_pairs: A list of pairs of chars that are present in both
    #           ``original_code`` and ``target_code``.
    #     - added_chars: A list of chars that have been added (are only present in ``target_code``)
    #     - removed_chars: A list of chars that have been removed (are only present in ``original_code``)
    #
    # Context
    #    1. The code_paragraph does not contain newlines as characters whereas code_strings do
    #    2. ``target_code`` has an ``encoded_string`` attribute that represents the changes
    #       from ``original_code`` to ``target_code``.
    #
    # Algorithm
    #    At a high level, after cleaning the code and strings, we iterate through the encoded
    #    string adding the char (VMobject) to its respective list.
    #
    # Example
    #    ``original_code`` (text representation of what the VMobject chars would look like when rendered)
    #    Notice the lack of newlines
    #    class Solution:
    #        def reverseList(self, head):
    #            if head is None or head.next is None:
    #                return head
    #
    #    ``target_code`` (text representation of what the VMobject chars would look like when rendered)
    #    Notice the lack of newlines
    #    class Solution:
    #        def reverseList(self, head):
    #            if head is None or head.next is None:
    #                return head
    #
    #            reverseList(head.next)
    #
    #   ``target_code.encoded_string``
    #    class Solution:\n
    #        def reverseList(self, head):\n
    #            if head is None or head.next is None:\n
    #                return head<A>\n
    #  </A>\n
    #  <A> </A><A> </A><A> </A><A> </A><A> </A><A> </A><A> </A><A> </A><A>r</A><A>e</A><A>v</A><A>e</A><A>r</A><A>s</A><A>e</A><A>L</A><A>i</A><A>s</A><A>t</A><A>(</A><A>h</A><A>e</A><A>a</A><A>d</A><A>.</A><A>n</A><A>e</A><A>x</A><A>t</A><A>)</A>
    original_code_chars = list(it.chain.from_iterable(original_code.code_paragraph))
    target_code_chars = list(it.chain.from_iterable(target_code.code_paragraph))

    target_code.encoded_string = target_code.encoded_string.replace(
        f"{TEXT_ADD_START_MARKER}\n{TEXT_ADD_END_MARKER}",
        "",
    )

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
