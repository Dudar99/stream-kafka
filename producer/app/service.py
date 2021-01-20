"""
Module where Flask application is created alongside with its endpoints
"""
import json
import producer

from flask import Flask, request

APP = Flask(__name__)


# just a smoke call that posts static json from file to default topic

@APP.route('/smoke_send', methods=['POST'])
def smoke_send():
    """
    Controller that handle /smoke_send POST call
    """
    producer.JsonKafkaProducer.send_smoke_data()
    return "Smoke message was sent!"


@APP.route('/send_message', methods=['POST'])
def send_message():
    """
    Controller that handle /send_message POST call, accepting JSON data as body
    """
    data = json.loads(request.data.decode('utf-8'))
    pr = producer.JsonKafkaProducer()
    pr.send(value=data)

    return "Message was sent!"
