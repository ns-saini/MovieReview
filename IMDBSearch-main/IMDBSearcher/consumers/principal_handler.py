import logging

from IMDBSearcher.consumers.handler import AbstractHandler
from IMDBSearcher.serializers import PrincipalSerializer


class PrincipalHandler(AbstractHandler):
    def handle(self, message):
        serializer = PrincipalSerializer(data=message)
        s = serializer.is_valid()
        if s:
            serializer.get
        else:
            logging.error(serializer.errors)

    def __init__(self, config):
        super().__init__(config)
        self.config = config


