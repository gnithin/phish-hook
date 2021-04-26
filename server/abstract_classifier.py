from abc import ABC, abstractmethod


class AbstractClassifier(ABC):
    """ Represents the structure of a classifier """

    @abstractmethod
    def predict(self, url) -> bool:
        pass