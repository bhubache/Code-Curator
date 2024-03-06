from __future__ import annotations

from collections.abc import Iterable
from types import GeneratorType


def flatten_iterable_parameters(args):
    flattened_parameters = []
    for arg in args:
        if isinstance(arg, (Iterable, GeneratorType)):
            flattened_parameters.extend(arg)
        else:
            flattened_parameters.append(arg)

    return flattened_parameters
