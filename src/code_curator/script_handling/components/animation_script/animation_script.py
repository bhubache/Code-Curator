from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Iterable


class AnimationScript(ABC):
    @property
    @abstractmethod
    def unique_id(self) -> str:
        pass

    @property
    @abstractmethod
    def text(self) -> str:
        pass

    @property
    @abstractmethod
    def num_words(self) -> int:
        pass

    @abstractmethod
    def get_flattened_iterable(self) -> Iterable:
        pass
