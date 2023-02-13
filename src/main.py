import argparse
import logging
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from json import load
from logging.config import dictConfig
from os.path import join, dirname, realpath

from servicebus import get_receiver, get_sender

logger = logging.getLogger(__name__)


def setup_logging():
    with open(join(dirname(realpath(__file__)), 'logging.json'), 'rt') as f:
        config = load(f)
        dictConfig(config)
        logging.Formatter.converter = time.gmtime


def parse_args():
    parser = argparse.ArgumentParser(description="Simple producer / consumer for debugging the azure servicebus")
    parser.add_argument("mode", choices=['producer', 'consumer'])
    args = parser.parse_args(sys.argv[1:])
    logger.info(f"Arguments: {args}")
    return args


def produce_messages(connection_string, queue_name):
    with get_sender(connection_string, queue_name) as send:
        while True:
            test = {'id': str(uuid.uuid4()), 'ts': float(datetime.now(tz=timezone.utc).timestamp())}
            send(test)
            time.sleep(1)


def consume_messages(connection_string, queue_name):
    with get_receiver(connection_string, queue_name) as receive:
        while True:
            message = receive()


def main():
    setup_logging()
    args = parse_args()

    connection_string = os.environ.get('CONNECTION_STRING', '')
    queue_name = os.environ.get('QUEUE_NAME', '')

    if args.mode == 'producer':
        produce_messages(connection_string, queue_name)
    elif args.mode == 'consumer':
        consume_messages(connection_string, queue_name)
    else:
        logger.error(f'Invalid mode: {args.mode}')


if __name__ == '__main__':
    main()
