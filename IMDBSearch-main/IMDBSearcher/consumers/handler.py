from abc import abstractmethod, ABC


class AbstractHandler(ABC):
    def __init__(self, config):
        self.config = config
        super().__init__()

    @abstractmethod
    def handle(self, message):
        pass