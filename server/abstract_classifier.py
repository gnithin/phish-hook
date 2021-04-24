from abc import ABC, abstractmethod


class AbstractClassifier(ABC):
    @abstractmethod
    def predict(self, url) -> bool:
        pass