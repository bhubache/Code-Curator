from abc import ABC, abstractmethod

class IAnimationScript(ABC):
    @abstractmethod
    def get_text(self) -> str:
        pass

    @abstractmethod
    def get_num_words(self) -> int:
        pass