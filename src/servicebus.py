import json
import logging
import timeit
from contextlib import contextmanager

from azure.servicebus import ServiceBusClient, ServiceBusMessage

logger = logging.getLogger(__name__)

@contextmanager
def get_receiver(connection_string, queue_name):
    with ServiceBusClient.from_connection_string(connection_string) as client, client.get_queue_receiver(
            queue_name=queue_name) as receiver:
        def receive_message():
            logger.info(f'Receiving message')
            start = timeit.default_timer()
            messages = receiver.receive_messages()
            stop = timeit.default_timer()
            if messages:
                message = json.loads(str(messages[0]))
                logger.info(f"Received message {message} in {stop - start}s")
                receiver.complete_message(messages[0])
                return message

        yield receive_message


@contextmanager
def get_sender(connection_string, queue_name):
    with ServiceBusClient.from_connection_string(connection_string) as client, client.get_queue_sender(
            queue_name) as sender:
        def send_message(m):
            message = ServiceBusMessage(body=json.dumps(m, default=lambda o: o.__dict__))
            logger.info(f'Sending message {m}')
            start = timeit.default_timer()
            sender.send_messages(message)
            stop = timeit.default_timer()
            logger.info(f'Sent message {m} in {stop - start}s')

        yield send_message
