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

    with get_session() as session:
        files = session.query(FileModel).all()

        try:
            files = session.query(FileModel).filter_by(collection=collection, path=path).all()
        except:
            session.rollback()
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
    #_session = sessionmaker(bind=engine)()

    with get_session() as _session:
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

            folder = FileModel(name=path, filename=name, collection=collection, type="folder", icon="fas fa-folder", path=_path, code="")
            _session.add(folder)
            _session.commit()

        return jsonify(folder)


@app.route('/files/<fid>', methods=['GET'])
def get_file(fid):
    with get_session() as session:
        file = session.query(FileModel).filter_by(id=fid).first()
        return file.code, 200

@app.route('/networks', methods=['GET'])
def get_networks():
    with get_session() as session:
        networks = []
        _networks = session.query(NetworkModel).all()

        for network in _networks:
            _network = {'label':network.name, 'id':network.id, 'icon':'fas fa-home'}
            networks += [_network]
            _network['children'] = []
            for node in network.nodes:
                _node = {'label':node.name, 'id':node.id, 'icon':'fas fa-home'}
                _agent = {'label':node.agent.name, 'id':node.agent.id, 'icon':'fas fa-user'}
                _node['children'] = [_agent]

                workers = []
                for worker in node.agent.workers:
                    _worker = {'label':worker.name, 'id':worker.id, 'icon':'fas fa-cog'}
                    _processor = {'label':worker.processor.name, 'id':worker.processor.id, 'icon':'fas fa-microchip'}

                    _worker['children'] = [_processor]
                    _processor['children'] = []
                    for socket in worker.processor.sockets:
                        _socket= {'label':socket.name, 'id':socket.id, 'icon':'outlet'}
                        _processor['children'] += [_socket]

                        _task = {'label':socket.task.name, 'id':socket.task.id, 'icon':'fas fa-check'}
                        _module = {'label':socket.task.module, 'id':socket.task.id+'module', 'icon':'fas fa-box'}
                        _function = {'label':socket.task.name, 'id':socket.task.id+'function', 'icon':'fab fa-python'}
                        _task['children'] = [_module]
                        _module['children'] = [_function]
                        _socket['children'] = [_task]

                    workers += [_worker]
                _agent['children'] = workers
                
                _network['children'] += [_node]

        return jsonify({'networks':networks})

@app.route('/files/<fid>', methods=['DELETE'])
def delete_file(fid):
    print("Deleting file",fid)
    with get_session() as session:
        try:
            file = session.query(FileModel).filter_by(id=fid).first()

            if file.type == 'folder':
                files = session.query(FileModel).filter_by(collection=file.collection, path=file.name).all()
                print("DELETE FOLDER PATH:",file.name," # FILES:",files)
                if len(files) > 0:
                    status = {'status':'error', 'message':'Folder not empty'}
                    print(status)
                    return jsonify(status), 500
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
    print("POST_NAME",path+"/"+data['name'])

    with get_session() as session:
        files = session.query(FileModel).all()
        for f in files:
            print("FILE:",f.path, f.name)
        if 'id' in data and (('saveas' in data and not data['saveas']) or 'saveas' not in data):
            print("FINDING FILE BY ID",data['id'])
            file = session.query(FileModel).filter_by(id=data['id']).first()
        else:
            print("FINDING FILE BY PATH",path+"/"+data['name'])
            file = session.query(FileModel).filter_by(name=path+"/"+data['name'], path=path, collection=collection, type=data['type']).first()
        print("FILE FOUND",file)
        if file:
            if ('id' in data and data['id'] == file.id) and ('saveas' in data and data['saveas']):
                # overwrite file
                print("Overwriting ",data)
                file.name=path+"/"+data['name']
                if 'file' not in data:
                    data['file'] = ""
                file.code=data['file']
                session.add(file)
                fid = file.id
                try:
                    session.commit()
                except:
                    error = {'status':'error','message':'Unable to overwrite file'}
                    session.rollback()
                    return jsonify(error), 409
            elif ('id' in data and data['id'] == file.id):
                print("Overwriting ",data)
                if 'file' not in data:
                    data['file'] = ""
                file.code=data['file']
                session.add(file)
                fid = file.id
                try:
                    session.commit()
                except:
                    error = {'status':'error','message':'Unable to overwrite file'}
                    session.rollback()
                    return jsonify(error), 409
            else:
                session.rollback()
                error = {'status':'error','message':'File name exists', 'id':file.id}
                return jsonify(error), 409

        else:
            file = FileModel(name=path+"/"+data['name'], filename=data['name'], collection=collection, type=data['type'], icon=data['icon'], path=path, code=data['file'])
            if 'saveas' in data:
                print("SAVEAS",file)
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
