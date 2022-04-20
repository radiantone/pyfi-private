"""
pyfi API server Flask app
"""
import logging
import platform
import json
from sqlalchemy.ext.declarative import DeclarativeMeta

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

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [
                x for x in dir(obj) if not x.startswith("_") and x != "metadata"
            ]:
                data = obj.__getattribute__(field)
                try:
                    # this will fail on non-encodable values, like other classes
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

app.json_encoder = AlchemyEncoder

@app.route('/files/<collection>/<path:path>', methods=['GET'])
def get_files(collection, path):
    print(collection, path)
    files = session.query(FileModel).filter_by(collection=collection, path=path).all()
    print("Files",files)
    return jsonify(files)


@app.route('/files/<collection>/<path:path>', methods=['POST'])
def post_files(collection, path):
    print("POST",collection, path)
    data = request.get_json(silent=True)
    print("POST_FILE",data)
    file = FileModel(name=data['name'], collection=collection, type=data['type'], icon=data['icon'], path=path, code=data['file'])
    session.add(file)
    session.commit()
    return "Ok", 200


@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('static/assets', path)


@app.route("/")
def hello():
    logging.debug("Invoking hello")
    return "Hi!"
