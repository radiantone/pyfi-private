import requests
import json
import configparser
from pathlib import Path

CONFIG = configparser.ConfigParser()

HOME = str(Path.home())
ini = HOME + "/pyfi.ini"
CONFIG.read(ini)

def get_queues():
    session = requests.Session()
    api = CONFIG.get("broker", "api")
    user = CONFIG.get("broker", "user")
    password = CONFIG.get("broker", "password")
    session.auth = (user,password)

    auth = session.post("http://localhost:15672")
    response = session.get("http://localhost:15672/api/queues")
    return json.loads(response.content)