"""
server.py - pyfi agent server
"""
import logging
import asyncio
from pyfi.celery.tasks import add
from pyfi.model import User
from pyfi.blueprints.show import blueprint
from pyfi.model import init_db

from flask import Flask, request, send_from_directory, current_app, send_from_directory

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.register_blueprint(blueprint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)


@app.route('/')
def hello():
    users = User.query.all()
    _users = ""
    for user in users:
        _users += "{}:{}".format(user.username, user.email)
        _users += "\n"
    logging.debug('Agent API')
    result = add.delay(4, 5)
    return "Hello World from agent!! {} {}".format(result.get(), _users)
