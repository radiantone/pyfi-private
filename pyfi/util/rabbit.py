import requests
import json
import configparser
from pathlib import Path

CONFIG = configparser.ConfigParser()

HOME = str(Path.home())
ini = HOME + "/pyfi.ini"
CONFIG.read(ini)

api = CONFIG.get("broker", "api")
base = api.replace('/api','')
user = CONFIG.get("broker", "user")
password = CONFIG.get("broker", "password")

def get_queues():
    session = requests.Session()
    session.auth = (user,password)

    auth = session.post(base)
    response = session.get(f"{api}/queues")
    return json.loads(response.content)


def get_messages(queue, count):
    session = requests.Session()
    session.auth = (user,password)

    auth = session.post(base)
    response = session.post(f"{api}/queues/%2F/{queue}/get", data='{"vhost":"/","name":"'+queue+'","truncate":"50000","ackmode":"ack_requeue_true","encoding":"auto","count":"'+count+'"}')
    return json.loads(response.content)