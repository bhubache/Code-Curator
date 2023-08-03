from __future__ import annotations


def partition(text: str, substring: str, occurrence: int | None = None) -> float:
    """Return [start, stop) of ``substring``."""
    if text.count(substring) > 1 and occurrence is None:
        raise ValueError(
            f'There is more than one occurrence of ``substring`` ``{substring}`` in ``{text}``,'
            ' yet an occurrence has not been specified. Please provide one.',
        )
    elif occurrence is None:
        occurrence = 1

    partition: tuple[str, str, str] = text.partition(substring)
    for _ in range(occurrence - 1):
        partition = _strip_elements(partition)

        sub_partition = partition[2].partition(substring)
        sub_partition = _strip_elements(sub_partition)

        partition = (
            ' '.join((partition[0], partition[1], sub_partition[0])),
            sub_partition[1],
            sub_partition[2],
        )

    return _strip_elements(partition)


def _strip_elements(partition: tuple[str, str, str]) -> tuple[str, str, str]:
    return tuple([s.strip() for s in partition])
