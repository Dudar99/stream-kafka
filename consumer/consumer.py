"""
Module implements custom kafka consumer
"""
import json

from utils import generate_json_unique_file_name
from os.path import abspath, join
from kafka import KafkaConsumer

# TODO make topic to be parametrized, not hard coded
TOPIC = 'json-stream'
SENSITIVE_DATA_FIELDS = ['name', 'address', 'latitude', 'longitude']


class JsonConsumer(KafkaConsumer):
    """
    Class that inherits all from KafkaConsumer and add override some default settings
    """

    def __init__(self, *topics, **config):
        config.update({'value_deserializer': self.__anonimize_confident_data,
                       'group_id': 'test-group',
                       'auto_offset_reset': 'earliest',
                       })
        super().__init__(*topics, **config)

    @classmethod
    def __anonimize_confident_data(cls, data):
        """
        Function that deserialize and anonimize data
            data: bytes object that consumer received when reading from topic
        """
        # TODO create some data encryption
        orig_data: dict = json.loads(data.decode('utf-8'))
        display_data = orig_data.copy()
        display_data.update({itm: 'REMOVED' for itm in SENSITIVE_DATA_FIELDS})
        return display_data

    @classmethod
    def read_json_data(cls, read_timeout_ms=10000):
        """
        Read portion of data and commit
            read_timeout_ms : number of milliseconds to wait until close connection and commit
        """
        data = []
        print(f"Starting reading messages from '{TOPIC}' topic.")
        consumer = JsonConsumer(TOPIC, enable_auto_commit=False, consumer_timeout_ms=read_timeout_ms)
        try:
            for message in consumer:
                print(f"Received message with offset: {message.offset}")
                data.append(message.value)
        finally:
            print(f"Finishing reading messages from '{TOPIC}' topic. Committing ..")
            consumer.commit()
        return data

    @classmethod
    def persist(cls, data: list):
        """
        Persists data in /data/persisted folder as .json files
            data: list of json items deserialized
        """
        if not data:
            print("Nothing to save.")
            return
        file_name = generate_json_unique_file_name(len(data))

        # TODO manage paths to be able to run from any floder , not just root fodler
        with open(join(abspath('data/persisted'), file_name), 'w+') as f:
            f.write(json.dumps(data))

        print(f"Saved {len(data)} records to {file_name}")
