from IMDBSearcher.consumers.handler import AbstractHandler
from IMDBSearcher.serializers import BasicSerializer


class BasicHandler(AbstractHandler):

    def handle(self, message):
        serializer = BasicSerializer(data=message)
        if serializer.is_valid():
            serializer.save()

    def __init__(self, config):
        super().__init__(config)
        self.config = config
