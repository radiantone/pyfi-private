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
from flask_restx import Api, Resource, fields, reqparse

request_parser = reqparse.RequestParser(bundle_errors=True)

logging.basicConfig(level=logging.INFO)

hostname = platform.node()

app = Flask(__name__)
app.register_blueprint(blueprint)

api = Api(app, version='1.0', title='LambdaFLOW API',
    description='LambdaFLOW Backend API',
)


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

def create_endpoint(modulename, taskname):
    # Query all processors with hasapi=True
    # for each proc
    # create namespace with proc.endpoint
    # Add wrapper class to dispatch call to processor task socket
    # Use decorator over class post method with parameters to the socket task
    # So it will invoke the class method with the correct runtime parameters


    def decorator(module="", task=""):
        from types import ModuleType

        with get_session() as session:
            _task = session.query(TaskModel).filter_by(name=task).first()
            code = _task.source

        print(code)
        mod = ModuleType(module, 'doc string here')
        exec(code, mod.__dict__)
        func = getattr(mod,task)

        def wrapper(cls, *args, **kwargs):
            
            cls.funcs[task] = func
            return cls


        return wrapper

    ns = api.namespace(modulename+'/'+taskname, description=taskname)
    route = ns.route('/')

    model = api.model('Message', {
        'name': fields.String,
    })

    @decorator(module=modulename, task=taskname)
    class FlowDelegate(Resource):
        funcs = {}
        
        @ns.expect(model)
        def post(self):
            # Fetch the socket and invoke that
            from pyfi.client.user import USER
            from pyfi.client.api import Socket
            logging.info("PAYLOAD",api.payload)
            socket = Socket(name=modulename+'.'+taskname, user=USER)
            if socket:
                logging.info("Invoking socket %s %s",modulename+'.'+taskname, socket)
                result = socket(api.payload)
                logging.info("Result %s",result)
                return result
            else:
                return self.funcs[taskname](api.payload)

    return route(FlowDelegate)    


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

@app.route('/processors', methods=['GET'])
def get_processors():

    with get_session() as session:
        processors = session.query(ProcessorModel).all()

        return jsonify(processors)


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


@app.route('/pattern/<pid>', methods=['GET'])
def get_pattern(pid):
    with open('pyfi/server/patterns/'+pid+'.json','r') as pattern:

        _pattern = json.loads(pattern.read())
        
        return jsonify(_pattern)

@app.route('/networks', methods=['GET'])
def get_networks():

    with get_session() as session:
        networks = []
        _networks = session.query(NetworkModel).all()

        for network in _networks:
            _network = {'label':network.name, 'tooltip':'Network', 'id':network.id, 'icon':'fas fa-home', 'data':json.loads(json.dumps(network, cls=AlchemyEncoder))}
            networks += [_network]
            _network['children'] = []
            for node in network.nodes:
                _node = {'label':node.name, 'tooltip':'Node', 'id':node.id, 'icon':'fas fa-cube', 'data':json.loads(json.dumps(node, cls=AlchemyEncoder))}
                _agent = {'label':node.agent.name, 'tooltip':'Agent', 'id':node.agent.id, 'icon':'fas fa-user'}
                _node['children'] = [_agent]

                workers = []
                for worker in node.agent.workers:
                    _worker = {'label':worker.name, 'tooltip':'Worker', 'id':worker.id, 'icon':'fas fa-hard-hat', 'data':json.loads(json.dumps(worker, cls=AlchemyEncoder))}
                    _processor = {'label':worker.processor.name, 'tooltip':'Processor', 'id':worker.processor.id, 'icon':'fas fa-microchip', 'data':json.loads(json.dumps(worker.processor, cls=AlchemyEncoder))}

                    _worker['children'] = [_processor]
                    _processor['children'] = []
                    for socket in worker.processor.sockets:
                        _socket= {'label':socket.name, 'tooltip':'Socket', 'id':socket.id, 'icon':'outlet', 'data':json.loads(json.dumps(socket, cls=AlchemyEncoder))}
                        _processor['children'] += [_socket]

                        _task = {'label':socket.task.name, 'tooltip':'Task', 'id':socket.task.id, 'icon':'fas fa-check', 'data':json.loads(json.dumps(socket.task, cls=AlchemyEncoder))}
                        _module = {'label':socket.task.module, 'tooltip':'Module', 'id':socket.task.id+'module', 'icon':'fas fa-box'}
                        _function = {'label':socket.task.name, 'tooltip':'Function', 'id':socket.task.id+'function', 'icon':'fab fa-python'}
                        _task['children'] = [_module]
                        _module['children'] = [_function]
                        _socket['children'] = [_task]

                    workers += [_worker]
                _agent['children'] = workers
                
                _network['children'] += [_node]

        print(networks)
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
            file = session.query(FileModel).filter_by(name=path+"/"+data['name'], path=path, collection=collection, type=data['type']).first()

            if file:
                error = {'status':'error','message':'File name exists', 'id':file.id}
                return jsonify(error), 409

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


class HelloService(Resource):
    def get(self, message):
        return f"Hello {message}"


hello = api.namespace('hello', description='Hello operations')
route = hello.route('/<string:message>')
route(HelloService)

''' Iterate over all the processors, tasks and for the ones where endpoint=True, add them as 
service routes. Perhaps monitor the database and update accordingly '''