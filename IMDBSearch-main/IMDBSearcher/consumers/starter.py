import logging
import threading

import pika

from IMDBSearch import settings
from IMDBSearcher.consumers.consumer import Consumer
from IMDBSearcher.consumers.name_handler import NameHandler


def start():
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    name_exchange = "name_exchange"
    queues = settings.RABBITMQ_QUEUES
    logging.debug(queues)

    for queue in queues:
        logging.info("Starting consumer for queue {}".format(queues[queue]))
        c = Consumer(name_exchange, queues[queue], credentials, settings.RABBITMQ_HOST, NameHandler(None))
        # c.start_consuming(cb=c.callback)
        threading.Thread(target=c.start_consuming,).start()
