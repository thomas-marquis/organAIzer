from abc import ABC, abstractmethod


class Agent(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError()