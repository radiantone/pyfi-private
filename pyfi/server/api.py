"""
pyfi API server Flask app
"""
import logging
import platform
from flask import Flask, jsonify, request, send_from_directory, current_app, send_from_directory

from pyfi.blueprints.show import blueprint
from pyfi.db.model import (
    oso,
    SchedulerModel,
    UserModel,
    EventModel,
    ArgumentModel,
    LoginModel,
    AgentModel,
    WorkerModel,
    CallModel,
    PlugModel,
    SocketModel,
    ProcessorModel,
    FileModel,
    NodeModel,
    RoleModel,
    QueueModel,
    TaskModel,
    LogModel,
    DeploymentModel,
    NetworkModel,
)
from pyfi.client.user import USER, engine, session

logging.basicConfig(level=logging.INFO)

hostname = platform.node()

app = Flask(__name__)
app.register_blueprint(blueprint)


@app.route('/files/<collection>/<path:path>', methods=['GET'])
def get_files(collection, path):
    print(collection, path)
    files = session.query(FileModel).filter_by(collection=collection, path=path).all()
    print("Files",files)
    files = []
    for i in range(0,50):
        files += [{
            'name':'File '+str(i),
            'id': i,
            '_id': i,
            'icon':'fas fa-file',
            'type':collection
        }]
    return jsonify(files)


@app.route('/files/<collection>/<path:path>', methods=['POST'])
def post_files(collection, path):
    print(collection, path)
    name=""
    file = FileModel(name=name, collection=collection, path=path)
    session.add(file)
    session.commit()
    return "Ok"


@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('static/assets', path)


@app.route("/")
def hello():
    logging.debug("Invoking hello")
    return "Hi!"
