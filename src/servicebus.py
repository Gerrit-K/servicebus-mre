import json
import logging
from contextlib import contextmanager

from azure.servicebus import AutoLockRenewer, ServiceBusClient, ServiceBusMessage

logger = logging.getLogger(__name__)

@contextmanager
def get_receiver(connection_string, queue_name):
    with ServiceBusClient.from_connection_string(connection_string) as client, AutoLockRenewer(
            max_lock_renewal_duration=5 * 60, max_workers=1) as auto_lock_renewer, client.get_queue_receiver(
        queue_name=queue_name, auto_lock_renewer=auto_lock_renewer) as receiver:
        def receive_message():
            messages = receiver.receive_messages()
            if messages:
                message = json.loads(str(messages[0]))
                logger.info(f"Received message {message}")
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
            sender.send_messages(message)
            logger.info(f'Sent message {m}')

        yield send_message
