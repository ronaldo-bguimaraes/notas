from abc import ABC, abstractmethod


class Step(ABC):
    def __init__(self, request):
        self.request = request

    @abstractmethod
    def handler(self):
        pass
