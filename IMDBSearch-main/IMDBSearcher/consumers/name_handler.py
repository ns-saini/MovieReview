import logging

from IMDBSearcher.consumers.handler import AbstractHandler
from IMDBSearcher.serializers import NamesSerializer


class NameHandler(AbstractHandler):

    def handle(self, message):
        serializer = NamesSerializer(data=message)
        s = serializer.is_valid()
        if s:
            serializer.save()
        else:
            logging.error(serializer.errors)

    def __init__(self, config):
        super().__init__(config)
        self.config = config


