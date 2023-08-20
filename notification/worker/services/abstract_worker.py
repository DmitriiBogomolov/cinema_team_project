from abc import ABC, abstractmethod


class AbstractWorker(ABC):

    @abstractmethod
    def send_message(*args, **kwargs):
        pass
