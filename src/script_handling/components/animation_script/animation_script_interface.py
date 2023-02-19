from abc import ABC, abstractmethod
from typing import Iterable

class IAnimationScript(ABC):
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