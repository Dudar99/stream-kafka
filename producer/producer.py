import json

from const import DEFAULT_PORT, DEFAULT_HOST, DEFAULT_TOPIC
from kafka import KafkaProducer


class JsonKafkaProducer(KafkaProducer):
    def __init__(self, **configs):
        configs.update({'bootstrap_servers': f'{DEFAULT_HOST}:{DEFAULT_PORT}',
                        'value_serializer': lambda m: json.dumps(m).encode('utf-8')})
        super().__init__(**configs)

    # can extend functionality here to support different schema validations and so on
    # or override parent class functionality
    def send(self, topic=DEFAULT_TOPIC, value=None, key=None, headers=None, partition=None, timestamp_ms=None):
        """
        Overridden .send() function just to use default topic
        """
        super().send(topic=DEFAULT_TOPIC, value=value, key=key, headers=headers, partition=partition,
                     timestamp_ms=timestamp_ms)

    @classmethod
    def send_smoke_data(cls):
        """
        Smoke function to test kafka producer
        """
        producer = JsonKafkaProducer()
        with open('/stream-kafka/data/sample1.json', 'r') as f:
            content = f.read()
            json_input = json.loads(content)
        producer.send(DEFAULT_TOPIC, value=json_input)

