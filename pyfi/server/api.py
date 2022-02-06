"""
pyfi API server Flask app
"""
import logging
import platform
import socket
from flask import Flask, request, send_from_directory, current_app, send_from_directory

from pyfi.blueprints.show import blueprint

logging.basicConfig(level=logging.INFO)

hostname = platform.node()

POSTGRES = "postgresql://postgres:pyfi101@" + hostname + ":5432/pyfi"

app = Flask(__name__)
app.register_blueprint(blueprint)


@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('static/assets', path)

@app.route("/")
def hello():
    logging.debug("Invoking hello")
    return "Hi!"