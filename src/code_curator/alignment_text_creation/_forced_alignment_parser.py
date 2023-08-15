"""Convert TextGrid from forced aligner aligned_script.txt."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from textgrids import TextGrid

if TYPE_CHECKING:
    from textgrids import Tier
    from textgrids import Interval


def create_aligned_script(textgrid_path: Path, output_file_path: Path) -> None:
    """Create aligned_script.txt.

    If there a silences found, the time they take up are
    given to the first word prior to the silences.
    """
    word_tier: Tier = TextGrid(textgrid_path)['words']

    word_tier = fix_initial_intervals(word_tier)

    cleaned_intervals: list[Interval] = [word_tier[0]]

    for curr_interval in word_tier[1:]:
        if curr_interval.text == '':
            continue

        cleaned_intervals[-1].xmax = curr_interval.xmin
        cleaned_intervals.append(curr_interval)

    write_aligned_script(intervals=cleaned_intervals, output_file_path=output_file_path)

    return output_file_path


def fix_initial_intervals(word_tier: Tier) -> Tier:
    """Get rid of empty strings at beginning of tier.

    Also, set xmin of first interval to 0.0.

    Args:
        word_tier: Contains all word intervals.

    Returns:
        word_tier: Initial intervals cleaned.
    """
    new_start_index: int = 0

    for interval in word_tier:
        if interval.text != '':
            break

        new_start_index += 1

    word_tier = word_tier[new_start_index:]
    word_tier[0].xmin = 0.0
    return word_tier


def write_aligned_script(intervals: list[Interval], output_file_path: Path) -> None:
    """Write aligned script to file.

    Args:
        intervals: All intervals that make up the aligned script.
        output_file_path: Path to resulting aligned script.

    Raises:
        ValueError: A gap in time is found between two intervals.
    """
    text_lines: list[str] = []

    for i, inter in enumerate(intervals):
        if i != len(intervals) - 1:
            if inter.xmax != intervals[i + 1].xmin:
                raise ValueError(f'There is a gap between {inter} and {intervals[i + 1]}')

        start: float = round(inter.xmin, 2)
        end: float = round(inter.xmax, 2)
        word: str = inter.text
        text_lines.append(f'{start}  {end}  {word}')

    with open(output_file_path, 'w', encoding='UTF-8') as write_file:
        write_file.write('\n'.join(text_lines))


def main():
    raise NotImplementedError('This cannot be run directly as a script yet.')


if __name__ == '__main__':
    create_aligned_script()
