from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any


class Weight(ABC):
    @property
    @abstractmethod
    def value(self) -> Any:
        pass

    @abstractmethod
    def get_color(self) -> Any:
        pass

    @abstractmethod
    def set_color(self, new_color: Any) -> None:
        pass
