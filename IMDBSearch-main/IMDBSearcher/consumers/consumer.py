import json

import pika
import os
import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IMDBSearch.settings")

from IMDBSearcher.consumers.handler import AbstractHandler


class Consumer:
    def __init__(self, exchange: str, queue_name: str, creds: pika.PlainCredentials, host: str,
                 service: AbstractHandler):
        self.exchange = exchange
        self.queue_name = queue_name
        self.connection = self.create_connection(creds, host)
        self.channel = self.create_channel()
        # self.create_queue()
        self.bind_channel_to_queue()
        self.routing_key = queue_name
        self.service = service

    def start(self):
        self.start_consuming(self.channel)

    def close(self):
        self.connection.close()

    def create_connection(self, creds: pika.PlainCredentials, host: str) -> pika.BlockingConnection:
        return pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=creds))

    def create_channel(self) -> pika.adapters.blocking_connection.BlockingChannel:
        return self.connection.channel()

    def create_queue(self):
        self.channel.queue_declare(queue=self.queue_name)
        logging.info("Queue {} created".format(self.queue_name))

    def bind_channel_to_queue(self):
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue_name, routing_key=self.queue_name)
        logging.info("Binded {} created to {}".format(self.queue_name, self.exchange))

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        data = json.loads(str(body, 'utf-8'))
        logging.info("Consuming: {}".format(str(body)))
        self.service.handle(data)
