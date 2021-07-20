"""
server.py - pyfi API server
"""
import logging
import asyncio
from pyfi.celery.tasks import add
from pyfi.blueprints.show import blueprint
from pyfi.model import init_db

from flask import Flask, request, send_from_directory, current_app, send_from_directory

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.register_blueprint(blueprint)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

'''
async def async_get_data():
    #await asyncio.sleep(1)
    return "Hello World!!!"

@app.route('/')
async def hello():
    data = await async_get_data()
    return data
'''

@app.route('/')
def hello():
    logging.debug('Invoking hello')
    result = add.delay(4,5)
    return "Hello World!! {}".format(result.get())
