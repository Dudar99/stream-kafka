import sys
import argparse
from consumer import JsonConsumer


def parse_args():
    """
    Parses arguments given application on startup
    :return: Namespace object with parameters - dest's
    """
    parser = argparse.ArgumentParser(description="Json Kafka consumerapplication", add_help=False)
    parser.add_argument("--help", action="help", help="show this help message and exit")

    parser.add_argument('--consumer-timeout-ms', default=10000, dest='consumer_timeout_ms', type=int)

    return parser.parse_args(sys.argv[1:])


if __name__ == '__main__':
    args = parse_args()
    consumer = JsonConsumer()
    data = consumer.read_json_data(read_timeout_ms=args.consumer_timeout_ms)
    consumer.persist(data)