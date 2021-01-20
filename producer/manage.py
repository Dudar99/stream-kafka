import argparse
import sys

from app.service import APP


def runserver(host, port):
    APP.run(host=host, port=port)


def parse_args():
    """
    Parses arguments given application on startup
    :return: Namespace object with parameters - dest's
    """
    parser = argparse.ArgumentParser(description="Flask server arguments", add_help=False)
    parser.add_argument("--help", action="help", help="show this help message and exit")
    parser.add_argument('-a', '--address', default='0.0.0.0', dest='host', type=str)
    parser.add_argument('-p', '--port', default=8001, dest='port', type=int)
    parser.add_argument('--kafka-address', dest='kafka_address', type=str)
    parser.add_argument('--kafka-port', dest='kafka_port', type=int)

    return parser.parse_args(sys.argv[1:])


def main():
    args = parse_args()
    runserver(host=args.host, port=args.port)


if __name__ == '__main__':
    main()
