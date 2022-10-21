import configparser
import json
from pathlib import Path

import requests

CONFIG = configparser.ConfigParser()

HOME = str(Path.home())
ini = HOME + "/pyfi.ini"
CONFIG.read(ini)

api = CONFIG.get("broker", "api")
base = api.replace("/api", "")
user = CONFIG.get("broker", "user")
password = CONFIG.get("broker", "password")


def purge_queue(queue):
    session = requests.Session()
    session.auth = (user, password)

    auth = session.post(base)
    response = session.delete(
        f"{api}/queues/%2F/{queue}/contents",
    )
    return response.content


def get_queues():
    session = requests.Session()
    session.auth = (user, password)

    auth = session.post(base)
    response = session.get(f"{api}/queues")
    return json.loads(response.content)


def get_messages(queue, count):
    session = requests.Session()
    session.auth = (user, password)

    auth = session.post(base)
    response = session.post(
        f"{api}/queues/%2F/{queue}/get",
        data='{"vhost":"/","name":"'
        + queue
        + '","ackmode":"ack_requeue_true","encoding":"auto","count":"'
        + str(count)
        + '"}',
    )
    return json.loads(response.content)
