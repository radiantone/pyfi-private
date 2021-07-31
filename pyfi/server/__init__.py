"""
pyfi API server Flask app
"""
import logging
import socket

from pyfi.celery.tasks import add
from pyfi.blueprints.show import blueprint

from flask import Flask, request, send_from_directory, current_app, send_from_directory

logging.basicConfig(level=logging.INFO)

hostname = socket.gethostbyname(socket.gethostname())

POSTGRES = 'postgresql://postgres:pyfi101@'+hostname+':5432/pyfi'

app = Flask(__name__)
app.register_blueprint(blueprint)

@app.route('/')
def hello():
    logging.debug('Invoking hello')
    result = add.delay(4,5)
    return "Hello World!! {}".format(result.get())
