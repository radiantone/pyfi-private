"""
pyfi API server Flask app
"""
import logging
import platform
import json
import gc
from sqlalchemy.ext.declarative import DeclarativeMeta

from contextlib import contextmanager
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
from pyfi.client.user import USER, engine, session, sessionmaker

logging.basicConfig(level=logging.INFO)

hostname = platform.node()

app = Flask(__name__)
app.register_blueprint(blueprint)

@contextmanager
def get_session(**kwargs):
    session = sessionmaker(bind=engine, **kwargs)()

    try:
        yield session
    except:
        session.rollback()
        raise
    else:
        session.commit()
    finally:
        session.expunge_all()
        session.close()
        gc.collect()

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
    files = session.query(FileModel).filter_by(collection=collection, path=path).all()
    print(files)
    def cmp_func(x):
        if x.type == 'folder':
            return 0
        else:
            return 1
    files = sorted(files, key=cmp_func)
    return jsonify(files)


@app.route('/folder/<collection>/<path:path>', methods=['GET'])
def new_folder(collection, path):
    _session = sessionmaker(bind=engine)()

    folder = _session.query(FileModel).filter_by(collection=collection, path=path, type="folder").first()
    print("FOLDER",folder)
    if not folder:
        name = path.rsplit('/')[-1:]
        _path = "/".join(path.rsplit('/')[:-1])
        if len(name) == 1:
            name = name[0]
        else:
            name = path
        print("NAME",name)
        folder = FileModel(name=name, collection=collection, type="folder", icon="fas fa-folder", path=_path, code="")
        _session.add(folder)
        _session.commit()

    return jsonify(folder)


@app.route('/files/<fid>', methods=['GET'])
def get_file(fid):
    file = session.query(FileModel).filter_by(id=fid).first()
    return file.code, 200


@app.route('/files/<fid>', methods=['DELETE'])
def delete_file(fid):
    print("Deleting file",fid)
    try:
        file = session.query(FileModel).filter_by(id=fid).first()
        if file:
            session.delete(file)
            session.commit()
            status = {'status':'ok'}
            return jsonify(status), 200
        else:
            status = {'status':'error', 'message':'Object not found '+fid}
            return jsonify(status), 404
    except Exception as ex:
        print(ex)
        status = {'status':'error', 'message':str(ex)}
        return jsonify(status), 500


@app.route('/files/<collection>/<path:path>', methods=['POST'])
def post_files(collection, path):
    print("POST",collection, path)
    data = request.get_json(silent=True)
    print("POST_FILE",data)
    file = session.query(FileModel).filter_by(name=data['name'], path=path, collection=collection, type=data['type']).first()
    if file:
        if 'id' in data and data['id'] == file.id:
            # overwrite file
            print("Overwriting ",data)
            file.name=data['name']
            if 'file' not in data:
                data['file'] = ""
            file.code=data['file']
            session.add(file)
            session.commit()
        else:
            error = {'status':'error','message':'File name exists'}
            return jsonify(error), 409

    else:
        file = FileModel(name=data['name'], collection=collection, type=data['type'], icon=data['icon'], path=path, code=data['file'])
        session.add(file)
        session.commit()

    status = {'status':'ok', 'id':file.id}
    print("STATUS",status)
    return jsonify(status)


@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('static/assets', path)


@app.route("/")
def hello():
    logging.debug("Invoking hello")
    return "Hi!"
