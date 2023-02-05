"""
pyfi API server Flask app
"""
import configparser
import json
import logging
import os
import platform
from base64 import b64decode, b64encode
from flasgger import Swagger

import chargebee
import requests

# from .chatgpt import configure

# configure()
chargebee.configure(os.environ["CB_KEY"], os.environ["CB_SITE"])

from functools import wraps
from typing import Any, Type

from flask import (
    Flask,
    _request_ctx_stack,
    jsonify,
    make_response,
    request,
    send_from_directory,
    session,
)
from flask_cors import cross_origin, CORS
from flask_restx import Api, Resource, fields, reqparse
from jose import JWTError, jwt
from six.moves.urllib.request import urlopen

from pyfi.blueprints.show import blueprint
from pyfi.client.user import USER
from pyfi.db import get_session
from pyfi.db.model import (
    AgentModel,
    AlchemyEncoder,
    CallModel,
    DeploymentModel,
    FileModel,
    NetworkModel,
    NodeModel,
    ProcessorModel,
    QueueModel,
    TaskModel,
    VersionModel,
    WorkerModel,
)

CONFIG = configparser.ConfigParser()
SESSION = session

from pathlib import Path

HOME = str(Path.home())
AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
API_AUDIENCE = os.environ['API_AUDIENCE']
ALGORITHMS = ["RS256"]

ini = HOME + "/pyfi.ini"

CONFIG.read(ini)

request_parser = reqparse.RequestParser(bundle_errors=True)

logging.basicConfig(level=logging.INFO)

hostname = platform.node()

app = Flask(__name__)
app.secret_key = "super secret key"
app.register_blueprint(blueprint)
cors = CORS(app, resources={r"/*": {"origins": "*.elasticcode.ai"}})

api = Api(
    app,
    version="1.0",
    title="ElasticCode API",
    description="ElasticCode Backend API",
)

setattr(app, "json_encoder", AlchemyEncoder)
template = {
    "swagger": "2.0",
    "info": {
        "title": "ElasticCode API",
        "description": "ElasticCode API",
        "contact": {
            "responsibleOrganization": "elasticcode.ai",
            "responsibleDeveloper": "darren@elasticcode.ai",
            "email": "support@elasticcode.ai",
            "url": "elasticcode.ai",
        },
        "termsOfService": "https://elasticcode.ai/terms",
        "version": "0.0.1"
    },
    "host": os.environ['API_HOST'],  # overrides localhost:500
    "basePath": "/",  # base bash for blueprint registration
    "schemes": [
        "https"
    ],
    "operationId": "getmyData"
}
swagger_config = {
    "title": "ElasticCode API",
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'processors',
            "route": '/processors',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "specs_route": "/ui",
    "url_prefix": "/docs"
}
swagger = Swagger(app=app, template=template, config=swagger_config)


# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header"""
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected",
            },
            401,
        )

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with" " Bearer",
            },
            401,
        )
    elif len(parts) == 1:
        raise AuthError(
            {"code": "invalid_header", "description": "Token not found"}, 401
        )
    elif len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be" " Bearer token",
            },
            401,
        )

    token = parts[1]
    return token


def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    return False


def requires_auth(f):
    """Determines if the Access Token is valid"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        try:
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks["keys"]:
                if (
                        "kid" in unverified_header
                        and key["kid"] == unverified_header["kid"]
                ):
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"],
                    }
            if rsa_key:
                try:
                    payload = jwt.decode(
                        token,
                        rsa_key,
                        algorithms=ALGORITHMS,
                        audience=API_AUDIENCE,
                        issuer="https://" + AUTH0_DOMAIN + "/",
                    )
                except jwt.ExpiredSignatureError:
                    raise AuthError(
                        {"code": "token_expired", "description": "token is expired"},
                        401,
                    )
                except jwt.JWTClaimsError:
                    raise AuthError(
                        {
                            "code": "invalid_claims",
                            "description": "incorrect claims,"
                                           "please check the audience and issuer",
                        },
                        401,
                    )
                except Exception:
                    raise AuthError(
                        {
                            "code": "invalid_header",
                            "description": "Unable to parse authentication" " token.",
                        },
                        401,
                    )

                if "user" not in SESSION:
                    user = requests.get(
                        payload["aud"][1], headers={"Authorization": "Bearer " + token}
                    ).json()
                    SESSION["user"] = b64encode(bytes(json.dumps(user), "utf-8"))

                _request_ctx_stack.top.current_user = payload
                return f(*args, **kwargs)
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to find appropriate key",
                },
                401,
            )
        except JWTError:
            raise AuthError(
                {"code": "invalid_jwt", "description": "Token did not validate"},
                401,
            )

    return decorated


def create_endpoint(modulename, taskname):
    # Query all processors with hasapi=True
    # for each proc
    # create namespace with proc.endpoint
    # Add wrapper class to dispatch call to processor task socket
    # Use decorator over class post method with parameters to the socket task
    # So it will invoke the class method with the correct runtime parameters

    def decorator(module="", task=""):
        import io
        from types import ModuleType

        with get_session() as session:
            _task = session.query(TaskModel).filter_by(name=task).first()

            if not _task:
                return

            code = _task.source

        code_lines = []
        inside_dec = False
        lines = io.StringIO(code).readlines()

        for line in lines:
            if line[0] == "@":
                inside_dec = True
            if inside_dec and line.find("def") != 0:
                continue
            else:
                code_lines += [line]
                inside_dec = False

        code = "".join(code_lines)
        mod = ModuleType(module, "doc string here")
        exec(code, mod.__dict__)
        func = getattr(mod, task)

        def wrapper(cls, *args, **kwargs):

            cls.funcs[task] = func
            return cls

        return wrapper

    ns = api.namespace(modulename + "/" + taskname, description=taskname)
    route = ns.route("/")

    model = api.model(
        "Message",
        {
            "message": fields.String,
        },
    )

    @decorator(module=modulename, task=taskname)
    class FlowDelegate(Resource):
        funcs = {}

        @ns.expect(model)
        def post(self):
            # Fetch the socket and invoke that
            from pyfi.client.api import Socket
            from pyfi.client.user import USER

            logging.info("PAYLOAD", api.payload)
            socket = Socket(name=modulename + "." + taskname, user=USER)
            if socket:
                logging.info(
                    "Invoking socket %s %s", modulename + "." + taskname, socket
                )
                result = socket(api.payload["message"])
                logging.info("Result %s", result)
                return result
            else:
                return self.funcs[taskname](api.payload)

    return route(FlowDelegate)


setattr(app, "json_encodore", AlchemyEncoder)


@app.route("/emptyqueue/<queuename>", methods=["GET"])
@cross_origin()
@requires_auth
def empty_queue(queuename):
    # send DELETE method to queue contents URL
    # http://<brokerurl>/api/queues/%2F/<queuename>/contents
    # Send queue status update to global pubsub channel
    return jsonify({"status": "ok"})


@app.route("/emptyqueues", methods=["GET"])
@cross_origin()
@requires_auth
def empty_queues():
    # Fetch all queues
    # send DELETE method to each queue
    return jsonify({"status": "ok"})


@app.route("/git/code", methods=["POST"])
@cross_origin()
@requires_auth
def get_code():
    from pydriller import Repository

    data: Any = request.get_json()

    repo = data["repo"]
    commit = data["commit"]

    r = Repository(repo, single=commit)

    for _commit in r.traverse_commits():
        for file in _commit.modified_files:
            return file.source_code

    return "No source code found", 404


@app.route("/git", methods=["POST"])
@cross_origin()
@requires_auth
def get_git():
    from pydriller import Repository

    data: Any = request.get_json()

    repo = data["repo"]
    file = data["file"]

    r = Repository(repo, filepath=file)

    commits = []

    for commit in r.traverse_commits():
        commits += [
            {
                "hash": commit.hash,
                "author": commit.author.name,
                "message": commit.msg,
                "date": str(commit.author_date),
            }
        ]

    commits.reverse()
    return jsonify(commits)


@app.route("/login/<id>", methods=["POST"])
@cross_origin()
@requires_auth
def login_processor(id):
    data: Any = request.get_json()

    password = data["password"]
    logging.info("LOGIN FOR %s %s", id, password)

    return jsonify({"status": "ok"})


@app.route("/processor/<name>", methods=["POST", "GET", "DELETE"])
@cross_origin()
@requires_auth
def do_processor(name):
    if request.method == "GET":
        with get_session() as session:
            _processor = session.query(ProcessorModel).filter_by(name=name).first()
            if _processor is None:
                return f"Processor {name} not found", 404

            return jsonify(_processor)

    if request.method == "POST":
        processor: Any = request.get_json()

        with get_session() as session:
            logging.info("POSTING processor: %s", processor)
            _processor = session.query(ProcessorModel).filter_by(name=name).first()

            if not _processor:

                props = {
                    "name": processor["name"],
                    "description": processor["description"],
                    "gitrepo": processor["gitrepo"],
                    "modulepath": processor["modulepath"],
                    "concurrency": processor["concurrency"],
                    "use_container": processor["container"],
                    "module": processor["package"],
                    "ratelimit": processor["ratelimit"],
                    "receipt": processor["receipt"],
                    "perworker": processor["perworker"],
                    "uistate": processor["uistate"],
                }
                _processor = ProcessorModel(**props, user=USER)
                session.add(_processor)
                return jsonify({"status": "ok"})
            else:
                logging.info("Updating processor %s with %s", _processor, processor)
                for key, value in processor.items():
                    if key != "id" and hasattr(_processor, key):
                        setattr(_processor, key, value)
                        logging.debug("Updated processor field %s with %s", key, value)

                session.add(_processor)
                return jsonify({"status": "ok"})


@app.route("/processors", methods=["GET"])
@cross_origin()
@requires_auth
def get_processors():
    """Example endpoint returning a list of processors
        This is using docstrings for specifications.
        ---
        definitions:
          Processor:
            type: object
            properties:
              name:
                type: string
        responses:
          200:
            description: A list of processors
            schema:
              $ref: '#/definitions/Processor'
            examples:
              processors: [{'name':'proc1'}]
    """
    with get_session() as session:
        processors = session.query(ProcessorModel).all()

        return jsonify(processors)


@app.route("/output/<resultid>", methods=["GET"])
@cross_origin()
@requires_auth
def get_output(resultid):
    import redis

    redisclient = redis.Redis.from_url(CONFIG.get("redis", "uri"))
    resultid = resultid.replace("celery-task-meta-", "")
    r = redisclient.get(resultid + "-output")
    logging.info("get_output: %s %s", resultid + "-output", r)
    response = make_response(r, 200)
    response.mimetype = "text/plain"
    return response


@app.route("/subscriptions/<user>", methods=["GET"])
@cross_origin()
@requires_auth
def get_subscription(user):
    import json

    user_bytes = b64decode(SESSION["user"])
    user = json.loads(user_bytes.decode("utf-8"))

    result = chargebee.Customer.list({"email[is]": user["email"]})
    customer_id = result[0].customer.id
    result = chargebee.Subscription.list({"customer_id[is]": customer_id})

    return str(result[0])


@app.route("/chatgpt", methods=["POST"])
@cross_origin()
@requires_auth
def consult_chatgpt():
    data = request.get_json()
    # answer = consult(data["question"])
    return """
Here is a function that will parse an english sentence


    import spacy
    
    def parse(sentence):
       return "The parsed sentence"

    
    """


@app.route("/result/<resultid>", methods=["GET"])
@cross_origin()
@requires_auth
def get_result(resultid):
    from pymongo import MongoClient

    # TODO: Change to mongo
    # redisclient = redis.Redis.from_url(CONFIG.get("redis", "uri"))
    # r = redisclient.get(resultid)
    client = MongoClient(CONFIG.get("mongodb", "uri"))
    logging.info("GETTING RESULT %s", resultid)
    with client:
        db = client.celery
        result = db.celery_taskmeta.find_one(
            {"task_id": resultid.replace("celery-task-meta-", "")}
        )
        logging.info("RESULT %s", result)

        _r = result["result"]

    return jsonify(_r)


@app.route("/files/<collection>/<path:path>", methods=["GET"])
@cross_origin()
@requires_auth
def get_files(collection, path):
    import json

    user_bytes = b64decode(SESSION["user"])
    user = json.loads(user_bytes.decode("utf-8"))

    with get_session(user=user) as session:

        try:
            files = (
                session.query(FileModel)
                .filter_by(collection=collection, path=path)
                .all()
            )
        except:
            session.rollback()
            files = (
                session.query(FileModel)
                .filter_by(collection=collection, path=path)
                .all()
            )

        print(files)

        def cmp_func(x):
            if x.type == "folder":
                return 0
            else:
                return 1

        files = sorted(files, key=cmp_func)
        return jsonify(files)


@app.route("/folder/<collection>/<path:path>", methods=["GET"])
@cross_origin()
@requires_auth
def new_folder(collection, path):
    with get_session() as _session:
        folder = (
            _session.query(FileModel)
            .filter_by(collection=collection, path=path, type="folder")
            .first()
        )
        if not folder:
            name = path.rsplit("/")[-1:]
            _path = "/".join(path.rsplit("/")[:-1])
            if len(name) == 1:
                name = name[0]
            else:
                name = path
            print("NAME", name)

            folder = FileModel(
                name=path,
                filename=name,
                collection=collection,
                type="folder",
                icon="fas fa-folder",
                path=_path,
                code="",
            )
            _session.add(folder)

        return jsonify(folder)


@app.route("/files/<fid>", methods=["GET"])
@cross_origin()
@requires_auth
def get_file(fid):
    with get_session() as session:
        file = session.query(FileModel).filter_by(id=fid).first()
        return file.code, 200


@app.route("/queue/<queue>/contents", methods=["DELETE"])
@cross_origin()
@requires_auth
def purge_queue(queue):
    from pyfi.util.rabbit import purge_queue

    return purge_queue(queue)


@app.route("/queue/messages/<queue>", methods=["GET"])
@cross_origin()
@requires_auth
def get_queue_messages(queue):
    import json

    from pyfi.util.rabbit import get_messages

    messages = get_messages(queue, 100)

    # Extract messages for queue
    print(json.dumps(messages, indent=4))
    if type(messages) is dict and "error" in messages:
        return f"Queue {queue} not found", 404

    _message = []
    print("MESSAGES", messages)
    for message in messages:
        msg = {}
        msg["payload"] = json.dumps(message, indent=4)
        msg["routing_key"] = message["routing_key"]
        msg["id"] = message["properties"]["headers"]["id"]
        kwargs = json.loads(
            message["properties"]["headers"]["kwargsrepr"].replace("'", '"')
        )
        msg["parent"] = kwargs["parent"]
        msg["tracking"] = kwargs["tracking"]
        msg["task"] = message["properties"]["headers"]["task"]

        if "postrun" in kwargs:
            msg["time"] = kwargs["postrun"]
        else:
            msg["time"] = ""
        _message += [msg]

    return jsonify(_message)


@app.route("/workers/<processor>", methods=["GET"])
@cross_origin()
@requires_auth
def get_workers(processor):
    with get_session() as session:
        _processor = session.query(ProcessorModel).filter_by(name=processor).first()
        if not _processor:
            return f"Processor {processor} not found", 404

        workers = session.query(WorkerModel).filter_by(processor_id=_processor.id).all()

        _workers = []

        for worker in workers:
            _workers += [
                {
                    "name": worker.name,
                    "host": worker.agent.hostname,
                    "cpus": "None" if not worker.deployment else worker.deployment.cpus,
                    "deployment": "None"
                    if not worker.deployment
                    else worker.deployment.name,
                    "status": worker.status,
                }
            ]
        return jsonify(_workers)


@app.route("/deployments/<processor>", methods=["GET"])
@cross_origin()
@requires_auth
def get_deployments(processor):
    with get_session() as session:
        _processor = session.query(ProcessorModel).filter_by(name=processor).first()
        deps = []

        if _processor:
            for dep in _processor.deployments:
                worker = dep.worker.name if dep.worker else "None"

                deps += [
                    {
                        "name": dep.name,
                        "owner": dep.owner,
                        "hostname": dep.hostname,
                        "cpus": dep.cpus,
                        "status": dep.worker.status if dep.worker else "None",
                        "worker": worker,
                    }
                ]

        return jsonify(deps)


@app.route("/pattern/<pid>", methods=["GET"])
@cross_origin()
@requires_auth
def get_pattern(pid):
    with open("pyfi/server/patterns/" + pid + ".json", "r") as pattern:
        _pattern = json.loads(pattern.read())

        return jsonify(_pattern)


@app.route("/code/extract", methods=["POST"])
@cross_origin()
@requires_auth
def code_extract():
    data = request.get_json(silent=True)
    code = data["code"]

    _funcs = {}

    return jsonify(_funcs)


@app.route("/deployments", methods=["GET"])
@cross_origin()
@requires_auth
def get_deploys():
    with get_session() as session:
        deployments = session.query(DeploymentModel).all()
        return jsonify(deployments)


@app.route("/queues", methods=["GET"])
@cross_origin()
@requires_auth
def get_queues():
    from pyfi.util.rabbit import get_queues as rabbit_queue_queues

    rabbit_queues = rabbit_queue_queues()

    with get_session() as session:
        queues = session.query(QueueModel).all()
        _queues = []

        for queue in queues:
            q = queue
            print("queue", queue.name)
            for rabbit_queue in rabbit_queues:
                if rabbit_queue["name"] == queue.name:
                    q = rabbit_queue
            _queues += [q]

        print(_queues)
        return jsonify(_queues)


@app.route("/agents", methods=["GET"])
@cross_origin()
@requires_auth
def get_agents():
    with get_session() as session:
        agents = session.query(AgentModel).all()
        return jsonify(agents)


@app.route("/workers", methods=["GET"])
@cross_origin()
@requires_auth
def get_workers_():
    with get_session() as session:
        workers = session.query(WorkerModel).all()
        return jsonify(workers)


@app.route("/tasks", methods=["GET"])
@cross_origin()
@requires_auth
def get_tasks():
    with get_session() as session:
        tasks = session.query(TaskModel).all()
        return jsonify(tasks)


@app.route("/nodes", methods=["GET"])
@cross_origin()
@requires_auth
def get_nodes():
    with get_session() as session:
        nodes = session.query(NodeModel).all()
        return jsonify(nodes)


@app.route("/networks", methods=["GET"])
@cross_origin()
@requires_auth
def get_networks():
    with get_session() as session:
        networks = []
        _networks = session.query(NetworkModel).all()

        for network in _networks:
            _network = {
                "label": network.name,
                "tooltip": "Network",
                "id": network.id,
                "icon": "fas fa-home",
                "data": json.loads(json.dumps(network, cls=AlchemyEncoder)),
            }
            networks += [_network]
            _network["children"] = []
            for node in network.nodes:
                _node = {
                    "label": node.name,
                    "tooltip": "Node",
                    "id": node.id,
                    "icon": "fas fa-cube",
                    "data": json.loads(json.dumps(node, cls=AlchemyEncoder)),
                }
                _agent = {
                    "label": node.agent.name,
                    "tooltip": "Agent",
                    "id": node.agent.id,
                    "icon": "fas fa-user",
                }
                _node["children"] = [_agent]

                workers = []
                for worker in node.agent.workers:
                    _worker = {
                        "label": worker.name,
                        "tooltip": "Worker",
                        "id": worker.id,
                        "icon": "fas fa-hard-hat",
                        "data": json.loads(json.dumps(worker, cls=AlchemyEncoder)),
                    }
                    _processor = {
                        "label": worker.processor.name,
                        "tooltip": "Processor",
                        "id": worker.processor.id,
                        "icon": "fas fa-microchip",
                        "data": json.loads(
                            json.dumps(worker.processor, cls=AlchemyEncoder)
                        ),
                    }

                    _worker["children"] = [_processor]
                    _processor["children"] = []
                    for socket in worker.processor.sockets:
                        _socket = {
                            "label": socket.name,
                            "tooltip": "Socket",
                            "id": socket.id,
                            "icon": "outlet",
                            "data": json.loads(json.dumps(socket, cls=AlchemyEncoder)),
                        }
                        _processor["children"] += [_socket]

                        _task = {
                            "label": socket.task.name,
                            "tooltip": "Task",
                            "id": socket.task.id,
                            "icon": "fas fa-check",
                            "data": json.loads(
                                json.dumps(socket.task, cls=AlchemyEncoder)
                            ),
                        }
                        _module = {
                            "label": socket.task.module,
                            "tooltip": "Module",
                            "id": socket.task.id + "module",
                            "icon": "fas fa-box",
                        }
                        _function = {
                            "label": socket.task.name,
                            "tooltip": "Function",
                            "id": socket.task.id + "function",
                            "icon": "fab fa-python",
                        }
                        _task["children"] = [_module]
                        _module["children"] = [_function]
                        _socket["children"] = [_task]

                    workers += [_worker]
                _agent["children"] = workers

                _network["children"] += [_node]

        print(networks)
        return jsonify({"networks": networks})


@app.route("/files/<fid>", methods=["DELETE"])
@cross_origin()
@requires_auth
def delete_file(fid):
    print("Deleting file", fid)
    with get_session() as session:
        try:
            file = session.query(FileModel).filter_by(id=fid).first()

            if file.type == "folder":
                files = (
                    session.query(FileModel)
                    .filter_by(collection=file.collection, path=file.name)
                    .all()
                )
                print("DELETE FOLDER PATH:", file.name, " # FILES:", files)
                if len(files) > 0:
                    status = {"status": "error", "message": "Folder not empty"}
                    print(status)
                    return jsonify(status), 500
            if file:
                session.delete(file)
                session.commit()
                status = {"status": "ok"}
                return jsonify(status), 200
            else:
                status = {"status": "error", "message": "Object not found " + fid}
                return jsonify(status), 404

        except Exception as ex:
            print(ex)
            status = {"status": "error", "message": str(ex)}
            return jsonify(status), 500


@app.route("/versions/<flowid>", methods=["GET"])
@cross_origin()
@requires_auth
def get_versions(flowid):
    with get_session() as session:
        logging.info("Getting versions for %s", flowid)
        versions = (
            session.query(VersionModel).filter(VersionModel.file_id == flowid).all()
        )
        logging.info("Got versions for %s %s", flowid, versions)

        _versions = [
            {
                "name": version.file.filename,
                "type": "flow",
                "filepath": version.file.path,
                "collection": version.file.collection,
                "version": str(version.version),
                "owner": version.owner,
                "code": version.flow,
            }
            for version in versions
        ]
        return jsonify(_versions)


@app.route("/calls/<name>", methods=["GET"])
@cross_origin()
@requires_auth
def get_calls(name):
    with get_session() as session:
        processor = session.query(ProcessorModel).filter_by(name=name).first()
        if not processor:
            return f"Processor {name} not found.", 404

        calls = (
            session.query(CallModel)
            .filter(CallModel.socket.has(processor_id=processor.id))
            .order_by(CallModel.created.desc())
            .limit(100)
            .all()
        )

        jcalls = jsonify(calls)
        return jcalls


@app.route("/registration", methods=["POST"])
def post_registration():
    from datetime import datetime
    from pymongo import MongoClient

    from pyfi.db.model import Base
    import hashlib
    from pyfi.db.model import UserModel

    data = request.get_json(silent=True)
    logging.info("REGISTRATION: %s", data)

    email = data['params']['user']['email']
    tenant = data['params']['user']['tenant']
    user_id = data['params']['user']['user_id']
    password = user_id.split('|')[1]
    client = MongoClient(CONFIG.get("mongodb", "uri"))
    pyfidb = client["pyfi"]
    users = pyfidb["users"]

    users.update_one({"email": email}, {'$set': data['params']['user']}, upsert=True)

    with get_session() as session:
        _password = hashlib.md5(password.encode()).hexdigest()
        # This user will be used in OSO authorizations
        uname = email.split('@')[0] + "." + password
        user = UserModel(
            name=uname, owner=email, password=_password, clear=password, email=email
        )
        users.insert_one()
        users.update_one({'_id': uname},
                         {'$set': {'_id': uname, 'email': email, 'user_id': user_id, 'password': password}},
                         upsert=True)

        user.lastupdated = datetime.now()
        sql = f"CREATE USER \"{uname}\" WITH PASSWORD '{password}'"
        logging.info("%s", sql)
        session.execute(sql)
        logging.info("Created user")
        for t in Base.metadata.sorted_tables:
            sql = f'GRANT CONNECT ON DATABASE pyfi TO \"{uname}\"'
            session.execute(sql)
            sql = f'GRANT SELECT, UPDATE, INSERT, DELETE ON "{t.name}" TO \"{uname}\"'
            session.execute(sql)
        session.add(user)

    logging.info("Commit ended")
    return "OK"


@app.route("/files/<collection>/<path:path>", methods=["POST"])
@cross_origin()
@requires_auth
def post_files(collection, path):
    print("POST", collection, path)
    data = request.get_json(silent=True)
    print("POST_FILE", data)
    print("POST_NAME", path + "/" + data["name"])

    with get_session() as session:
        files = session.query(FileModel).all()
        if "id" in data and (
                ("saveas" in data and not data["saveas"]) or "saveas" not in data
        ):
            print("FINDING FILE BY ID", data["id"])
            file = session.query(FileModel).filter_by(id=data["id"]).first()
        else:
            print("FINDING FILE BY PATH", path + "/" + data["name"])
            file = (
                session.query(FileModel)
                .filter_by(
                    name=path + "/" + data["name"],
                    path=path,
                    collection=collection,
                    type=data["type"],
                )
                .first()
            )
        print("FILE FOUND", file)
        if file:
            if ("id" in data and data["id"] == file.id) and (
                    "saveas" in data and data["saveas"]
            ):
                # overwrite file
                print("Overwriting ", data)
                file.name = path + "/" + data["name"]
                if "file" not in data:
                    data["file"] = ""
                file.code = data["file"]
                session.add(file)
                fid = file.id
                try:
                    session.commit()
                    print("Committed")
                except:
                    import traceback

                    print(traceback.format_exc())
                    error = {"status": "error", "message": "Unable to overwrite file"}
                    session.rollback()
                    return jsonify(error), 409
            elif "id" in data and data["id"] == file.id:
                print("Overwriting ", data)
                if "file" not in data:
                    data["file"] = ""
                file.code = data["file"]
                session.add(file)
                fid = file.id
                try:
                    session.commit()
                except:
                    import traceback

                    print(traceback.format_exc())
                    error = {"status": "error", "message": "Unable to overwrite file"}
                    session.rollback()
                    return jsonify(error), 409
            else:
                session.rollback()
                error = {
                    "status": "error",
                    "message": "File name exists",
                    "id": file.id,
                }
                return jsonify(error), 409

        else:
            file = (
                session.query(FileModel)
                .filter_by(
                    name=path + "/" + data["name"],
                    path=path,
                    collection=collection,
                    type=data["type"],
                )
                .first()
            )

            if file:
                error = {
                    "status": "error",
                    "message": "File name exists",
                    "id": file.id,
                }
                return jsonify(error), 409

            file = FileModel(
                name=path + "/" + data["name"],
                filename=data["name"],
                collection=collection,
                type=data["type"],
                icon=data["icon"],
                path=path,
                code=data["file"],
                user=USER
            )

            if "saveas" in data:
                print("SAVEAS", file)

        if data["type"] == "flow":
            logging.info("Creating version %s %s", file.name, file.id)
            version = VersionModel(name=file.name, file=file, flow=file.code)
            session.add(version)
            logging.info("Added version %s", version)

        session.add(file)
        try:
            session.commit()
        except Exception as ex:
            print(ex)

        status = {"status": "ok", "id": file.id}
        print("STATUS", status)
        return jsonify(status)


@app.route("/assets/<path:path>")
def send_js(path):
    return send_from_directory("static/assets", path)


class HelloService(Resource):
    def get(self, message):
        return f"Hello {message}"


hello = api.namespace("hello", description="Hello operations")
route = hello.route("/<string:message>")
route(HelloService)

""" Iterate over all the processors, tasks and for the ones where endpoint=True, add them as
service routes. Perhaps monitor the database and update accordingly """
