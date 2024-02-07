"""
pyfi API server Flask app
"""
import configparser
import json
import logging
import os
import platform
from base64 import b64decode, b64encode
from multiprocessing import Condition

import chargebee
import mindsdb_sdk
import redis
import requests
from flasgger import Swagger

lock = Condition()


# connects to the specified host and port
server = mindsdb_sdk.connect(os.environ["MINDSDB_SERVER"])
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
)
from flask import session as SESSION
from flask_cors import CORS, cross_origin
from flask_restx import Api, Resource, fields, reqparse
from jose import JWTError, jwt
from six.moves.urllib.request import urlopen

from flask_session import Session
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

from pathlib import Path

HOME = str(Path.home())
AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
API_AUDIENCE = os.environ["API_AUDIENCE"]
ALGORITHMS = ["RS256"]

ini = HOME + "/pyfi.ini"

CONFIG.read(ini)
SQLALCHEMY_DATABASE_URI = CONFIG.get("database", "uri")
request_parser = reqparse.RequestParser(bundle_errors=True)

redisclient = redis.Redis.from_url(CONFIG.get("redis", "uri"))

logging.basicConfig(level=logging.INFO)

hostname = platform.node()

app = Flask(__name__)
app.config["SESSION_TYPE"] = "redis"
app.config["SECRET_KEY"] = "super secret key"
app.config["SESSION_REDIS"] = redisclient
app.register_blueprint(blueprint)
Session(app)
cors = CORS(app, resources={r"/*": {"origins": "*.elasticcode.ai"}})
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = 60  # in seconds

api = Api(
    app,
    version="1.0",
    title="ElasticCode API",
    description="ElasticCode Backend API",
)

setattr(app, "json_encoder", AlchemyEncoder)
template = {
    "swagger": "2.0",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "in": "header",
        }
    },
    "security": [{"Bearer": []}],
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
        "version": "0.0.1",
    },
    "host": os.environ["API_HOST"],  # overrides localhost:500
    "basePath": "/",  # base bash for blueprint registration
    "schemes": ["https", "http"],
    "operationId": "getmyData",
}

swagger_config = {
    "title": "ElasticCode API",
    "headers": [],
    "specs": [
        {
            "endpoint": "execute",
            "route": "/execute",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "specs_route": "/ui",
    "url_prefix": "/docs",
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


def hasPlan(plan):
    sub = SESSION["subscription"]
    print(sub)
    return True


def requires_subscription(*args, **kwargs):
    """Determines if the Access Token is valid"""

    def decorated(f, *args, **kwargs):
        if request:
            sub = SESSION["subscription"]
        return f

    return decorated


def requires_auth(f):
    """Determines if the Access Token is valid"""

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            lock.acquire()

            token = get_token_auth_header()

            print(
                "SESSION['user']",
                SESSION,
                SESSION["user"] if "user" in SESSION else None,
            )

            if "user" in SESSION and SESSION["user"] is not None:
                return f(*args, **kwargs)

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
                            {
                                "code": "token_expired",
                                "description": "token is expired",
                            },
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
                                "description": "Unable to parse authentication"
                                " token.",
                            },
                            401,
                        )

                    if "user" not in SESSION or SESSION["user"] is None:
                        user = requests.get(
                            payload["aud"][1],
                            headers={"Authorization": "Bearer " + token},
                        ).json()
                        print("SESSION", SESSION)
                        SESSION["user"] = b64encode(bytes(json.dumps(user), "utf-8"))

                    print(SESSION["user"])
                    _request_ctx_stack.top.current_user = payload
                    return f(*args, **kwargs)
                raise AuthError(
                    {
                        "code": "invalid_header",
                        "code": "invalid_header",
                        "description": "Unable to find appropriate key",
                    },
                    401,
                )
            except JWTError as ex:
                if "user" in SESSION:
                    del SESSION["user"]
                logging.error(ex)
                raise AuthError(
                    {"code": "invalid_jwt", "description": "Token did not validate"},
                    401,
                )
        finally:
            lock.release()

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


@app.route("/logout", methods=["GET"])
@cross_origin()
@requires_auth
def logout():
    SESSION.clear()
    return jsonify({"status": "ok"})


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


@app.route("/runblock", methods=["POST"])
@cross_origin()
def run_block():
    """Run a given block in a container and return the result"""
    import os
    from uuid import uuid4

    import docker

    block = request.get_json()

    client = docker.from_env()

    _uuid = str(uuid4())
    try:
        with open("/tmp/" + _uuid, "w") as pfile:
            pfile.write(block["block"]["code"] + "\n\n")
            pfile.write(block["call"] + "\n")
            print(block["block"]["code"] + "\n\n")
            print(block["call"] + "\n")

        result = client.containers.run(
            block["block"]["containerimage"],
            auto_remove=False,
            volumes={"/tmp": {"bind": "/tmp/", "mode": "rw"}},
            entrypoint="",
            command="python /tmp/" + _uuid,
        )
        result = result.decode("utf-8").strip()
        return result
    finally:
        os.remove("/tmp/" + _uuid)


@app.route("/execute", methods=["GET"])
@cross_origin()
@requires_auth
def execute_flow():
    """Execute a saved flow
    Execute a Flow and return the results.
    ---
    definitions:
      Result:
        type: object
        properties:
          name:
            id: string
      Flow:
        type: object
        properties:
          name:
            type: string
    responses:
      200:
        description: JSON Result of Flow
        schema:
          $ref: '#/definitions/Result'
        examples:
          result: [{'some':'data'}]
    """
    result = []

    return jsonify(result)


@app.route("/processors", methods=["GET"])
@cross_origin()
@requires_auth
def get_processors():
    """Example endpoint returning a list of processors"""
    with get_session() as session:
        processors = session.query(ProcessorModel).all()

        return jsonify(processors)


@app.route("/output/<resultid>", methods=["GET"])
@cross_origin()
@requires_auth
def get_output(resultid):
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

    try:
        lock.acquire()

        result = chargebee.Customer.list({"email[is]": user["email"]})
        if len(result) == 0:
            return jsonify(
                {
                    "error": "true",
                    "subscription": "false",
                    "message": "No subscriptin for this user",
                }
            )

        customer_id = result[0].customer.id
        result = chargebee.Subscription.list({"customer_id[is]": customer_id})
        _sub = str(result[0])
        SESSION["subscription"] = _sub
        return _sub
    finally:
        lock.release()


@app.route("/health", methods=["GET"])
def health():
    return "OK", 200


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


@app.route("/stats/<stat>", methods=["GET"])
@cross_origin()
@requires_auth
def get_stats(stat):
    status = {"status": "ok"}
    return jsonify(status), 200


@app.route("/files/<collection>/<path:path>", methods=["GET"])
@cross_origin()
@requires_auth
def get_files(collection, path):
    import json

    from pyfi.db.model import UserModel

    user_bytes = b64decode(SESSION["user"])
    user = json.loads(user_bytes.decode("utf-8"))

    try:
        lock.acquire()

        with get_session(user=user) as session:
            password = user["sub"].split("|")[1]
            uname = user["email"].split("@")[0] + "." + password
            _user = (
                session.query(UserModel).filter_by(name=uname, clear=password).first()
            )
            try:
                files = (
                    session.query(FileModel)
                    .filter_by(collection=collection, path=path, user=_user)
                    .all()
                )
            except:
                session.rollback()
                files = (
                    session.query(FileModel)
                    .filter_by(collection=collection, path=path, user=_user)
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
    finally:
        lock.release()


@app.route("/folder/<collection>/<path:path>", methods=["GET"])
@cross_origin()
@requires_auth
def new_folder(collection, path):
    from pyfi.db.model import Base, UserModel

    user_bytes = b64decode(SESSION["user"])
    user = json.loads(user_bytes.decode("utf-8"))
    with get_session() as _session:
        folder = (
            _session.query(FileModel)
            .filter_by(collection=collection, path=path, type="folder")
            .first()
        )
        if not folder:
            name = path.rsplit("/")[-1:]
            password = user["sub"].split("|")[1]
            uname = user["email"].split("@")[0] + "." + password

            _path = "/".join(path.rsplit("/")[:-1])

            _user = (
                _session.query(UserModel).filter_by(name=uname, clear=password).first()
            )
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
                user=_user,
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


@app.route("/db/submit", methods=["POST"])
@cross_origin()
@requires_auth
def db_submit():
    import warnings

    import sqlalchemy
    from pandas import json_normalize

    # Create the engine to connect to the PostgreSQL database
    data = request.get_json(silent=True)

    dburl = data["database"]["url"]
    table = data["database"]["table"]
    rows = data["data"]

    engine = sqlalchemy.create_engine(dburl)

    df = json_normalize(rows)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        df.to_sql(
            table,
            con=engine,
            if_exists="append",
            index=False,
        )

    print(data)
    return jsonify({"operation": "commit", "status": "success"})


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


@app.route("/rename/flow/<flowid>", methods=["POST"])
@cross_origin()
@requires_auth
def rename_flow(flowid):

    data = request.get_json(silent=True)

    with get_session() as session:
        flow = session.query(FileModel).filter(FileModel.id == flowid).first()
        flow.filename = data["name"]
        session.add(flow)
        session.commit()

        status = {"status": "ok", "id": flowid}
        return jsonify(status)


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
    import hashlib
    from datetime import datetime

    # from pymongo import MongoClient
    import sqlalchemy

    from pyfi.db.model import Base, UserModel

    data = request.get_json(silent=True)
    logging.info("REGISTRATION: %s", data)

    email = data["params"]["user"]["email"]
    tenant = data["params"]["user"]["tenant"]
    user_id = data["params"]["user"]["user_id"]
    password = user_id.split("|")[1]
    # client = MongoClient(CONFIG.get("mongodb", "uri"))
    # pyfidb = client["pyfi"]
    # users = pyfidb["users"]

    # users.update_one({"email": email}, {'$set': data['params']['user']}, upsert=True)

    with get_session() as session:
        _password = hashlib.md5(password.encode()).hexdigest()
        # This user will be used in OSO authorizations
        uname = email.split("@")[0] + "." + password
        user = UserModel(
            name=uname,
            owner=email,
            password=_password,
            clear=password,
            email=email,
            id=user_id,
        )
        # users.update_one({'_id': uname},
        #                 {'$set': {'_id': uname, 'email': email, 'user_id': user_id, 'password': password}},
        #             upsert=True)

        user.lastupdated = datetime.now()
        sql = f"CREATE USER \"{uname}\" WITH PASSWORD '{password}'"
        try:
            logging.info("%s", sql)
            try:
                session.execute(sql)
                logging.info("Created user")
            except sqlalchemy.exc.IntegrityError as ex:
                if ex.orig.pgerror.find("already exists") == -1:
                    raise ex

            for t in Base.metadata.sorted_tables:
                sql = f'GRANT CONNECT ON DATABASE pyfi TO "{uname}"'
                session.execute(sql)
                sql = f'GRANT SELECT, UPDATE, INSERT, DELETE ON "{t.name}" TO "{uname}"'
                session.execute(sql)
        except sqlalchemy.exc.ProgrammingError as ex:
            if ex.orig.pgerror.find("already exists") == -1:
                raise ex

        session.add(user)

        result = chargebee.Customer.create({"email": email})
        result = chargebee.Subscription.create_with_items(
            result.customer.id,
            {
                "subscription_items": [
                    {
                        "item_price_id": "ec_free-USD-Monthly",
                        "quantity": 1,
                        "unit_price": 0,
                    }
                ]
            },
        )
    logging.info("Commit ended")
    return "OK"


@app.route("/files/<collection>/<path:path>", methods=["POST"])
@cross_origin()
@requires_auth
def post_files(collection, path):
    from pyfi.db.model import UserModel

    print("POST", collection, path)
    data = request.get_json(silent=True)
    print("POST_FILE", data)
    print("POST_NAME", path + "/" + data["name"])

    user_bytes = b64decode(SESSION["user"])
    user = json.loads(user_bytes.decode("utf-8"))

    try:
        with get_session(user=user) as session:
            password = user["sub"].split("|")[1]
            uname = user["email"].split("@")[0] + "." + password
            _user = (
                session.query(UserModel).filter_by(name=uname, clear=password).first()
            )

            if "id" in data and (
                ("saveas" in data and not data["saveas"]) or "saveas" not in data
            ):
                print("FINDING FILE BY ID", data["id"])
                file = (
                    session.query(FileModel)
                    .filter_by(id=data["id"], user=_user)
                    .first()
                )
            else:
                print("FINDING FILE BY PATH", path + "/" + data["name"])
                file = (
                    session.query(FileModel)
                    .filter_by(
                        name=path + "/" + data["name"],
                        path=path,
                        collection=collection,
                        type=data["type"],
                        user=_user,
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
                        error = {
                            "status": "error",
                            "message": "Unable to overwrite file",
                        }
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
                        error = {
                            "status": "error",
                            "message": "Unable to overwrite file",
                        }
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
                        user=_user,
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
                    user=_user,
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
                return jsonify({"status": "error", "message": str(ex)}), 500

            status = {"status": "ok", "id": file.id}
            print("STATUS", status)
            return jsonify(status)
    except Exception as ex:
        return jsonify({"status": "error", "message": str(ex)})


@app.route("/minds/database/<database>/<table>", methods=["POST"])
@cross_origin()
@requires_auth
def create_table(database, table):

    data: Any = request.get_json()

    db = server.get_database(database)

    query = db.query(data["query"])
    db.create_table(table, query)
    status = {"status": "ok"}
    return jsonify(status)


@app.route("/minds/database", methods=["POST"])
@cross_origin()
@requires_auth
def create_database():
    from pymongo import MongoClient

    client = MongoClient(CONFIG.get("mongodb", "uri"))
    data: Any = request.get_json()

    try:
        with get_session() as session:
            dbname = data["dbname"]
            try:
                session.execute(f"CREATE DATABASE {dbname}")
            except:
                # Ignore if exists
                pass
            client["mindsdb"]["databases"].insert_one(data)

            if data["dbtype"] == "Postgres":
                mdb = server.create_database(
                    engine=data["dbtype"],
                    name=data["dbname"],
                    connection_args={
                        "host": data["dbhost"],
                        "port": data["dbport"],
                        "database": data["dbname"],
                        "user": data["dbuser"],
                        "password": data["dbpwd"],
                    },
                )

                status = {"status": "ok", "message": "Database created successfully!"}
                return jsonify(status)
            if data["dbtype"] == "SQLite":
                mdb = server.create_database(
                    engine=data["dbtype"],
                    name=data["dbname"],
                    connection_args={"db_file": data["dbname"]},
                )

                status = {"status": "ok", "message": "Database created successfully!"}
                return jsonify(status)
    except Exception as ex:
        msg = str(ex)
        status = {"status": "error", "message": msg}
        return jsonify(status), 500


@app.route("/minds/database", methods=["DELETE"])
@cross_origin()
@requires_auth
def delete_database():
    pass


@app.route("/minds/projects", methods=["GET"])
@cross_origin()
@requires_auth
def list_projects():
    import itertools

    counter = itertools.count(0)

    projects = server.list_projects()

    names = [
        {
            "label": project.name,
            "name": project.name,
            "icon": "las la-clipboard",
            "lazy": True,
            "type": "project",
            "id": "proj{}".format(next(counter)),
        }
        for project in projects
    ]

    return jsonify(names)


@app.route("/minds/project/<project>/models", methods=["GET"])
@cross_origin()
@requires_auth
def list_models(project):

    import itertools

    counter = itertools.count(0)

    project = server.get_project(project)
    try:
        models = project.list_models()

        names = [
            {
                "label": model.name,
                "name": model.name,
                "icon": "las la-cube",
                "lazy": True,
                "type": "model",
                "status": model.get_status(),
                "id": "model{}".format(next(counter)),
            }
            for model in models
        ]

        return jsonify(names)
    except:
        return jsonify([])


@app.route("/minds/project/<project>/views", methods=["GET"])
@cross_origin()
@requires_auth
def list_views(project):

    import itertools

    counter = itertools.count(0)

    project = server.get_project(project)
    try:
        views = project.list_views()

        names = [
            {
                "label": view.name,
                "name": view.name,
                "icon": "las la-table",
                "lazy": True,
                "type": "view",
                "id": "view{}".format(next(counter)),
            }
            for view in views
        ]

        return jsonify(names)
    except:
        return jsonify([])


@app.route("/minds/project/<project>/jobs", methods=["GET"])
@cross_origin()
@requires_auth
def list_jobs(project):

    import itertools

    counter = itertools.count(0)

    project = server.get_project(project)
    try:
        jobs = project.list_jobs()

        names = [
            {
                "label": job.name,
                "name": job.name,
                "icon": "las la-table",
                "lazy": True,
                "type": "job",
                "id": "job{}".format(next(counter)),
            }
            for job in jobs
        ]

        return jsonify(names)
    except:
        return jsonify([])


@app.route("/minds/<project>/model/<model>", methods=["GET"])
@cross_origin()
@requires_auth
def get_model(project, model):
    project = server.get_project(project)

    return jsonify(project.get_model(model))


@app.route("/minds/<project>/models/<model>/<limit>", methods=["GET"])
@cross_origin()
@requires_auth
def get_predictions(project, model, limit=25):
    from pymongo import MongoClient

    client = MongoClient(CONFIG.get("mongodb", "uri"))

    _project = server.get_project(project)

    _model = _project.get_model(model)
    _dbmodel = client["mindsdb"]["models"].find_one({"project": project, "name": model})
    database = server.get_database(_dbmodel["database"])
    table = database.get_table(_dbmodel["table"])

    predictions = _model.predict(table.limit(int(limit)))

    return jsonify(predictions.to_dict())


@app.route("/minds/<project>/models/<model>", methods=["POST"])
@cross_origin()
@requires_auth
def get_prediction(project, model):
    import pandas as pd

    data: Any = request.get_json()

    _project = server.get_project(project)

    _model = _project.get_model(model)

    values = data["data"]
    result = _model.predict(pd.DataFrame.from_records([values]))
    _r = result.to_dict()
    return jsonify(_r)


@app.route("/minds/<project>/model/<model>/status", methods=["GET"])
@cross_origin()
@requires_auth
def get_model_status(project, model):
    project = server.get_project(project)

    model = project.get_model(model)

    return jsonify(model.get_status())


@app.route("/minds/<project>/model/<model>/info", methods=["GET"])
@cross_origin()
@requires_auth
def get_model_info(project, model):
    project = server.get_project(project)

    model = project.get_model(model)

    return jsonify(model.describe())


@app.route("/minds/<project>/model/<model>/refresh", methods=["POST"])
@cross_origin()
@requires_auth
def refresh_model(project, model):
    project = server.get_project(project)

    model = project.get_model(model)

    return jsonify(model.refresh())


@app.route("/minds/project/<project>/model/retrain/<model>", methods=["POST"])
@cross_origin()
@requires_auth
def retrain_model(project, model):
    _project = server.get_project(project)

    _model = _project.get_model(model)
    _model.retrain()
    return jsonify(
        {
            "project": project,
            "model": model,
            "operation": "training",
            "status": "success",
        }
    )


@app.route("/minds/<project>/model/<model>", methods=["DELETE"])
@cross_origin()
@requires_auth
def delete_model(project, model):
    project = server.get_project(project)

    return jsonify(project.drop_model(model))


@app.route("/minds/database/<database>/<table>/<limit>", methods=["GET"])
@cross_origin()
@requires_auth
def get_table(database, table, limit):
    database = server.get_database(database)

    _table = database.get_table(table)

    _table.limit(limit)
    return jsonify(_table.fetch())


@app.route("/minds/database/<database>/tables", methods=["GET"])
@cross_origin()
@requires_auth
def list_tables(database):
    import itertools

    counter = itertools.count(0)

    database = server.get_database(database)

    tables = database.list_tables()
    tables = list(set([table.name for table in tables]))
    names = [
        {
            "label": table,
            "name": table,
            "icon": "las la-table",
            "lazy": True,
            "type": "table",
            "id": "table{}".format(next(counter)),
        }
        for table in tables
    ]

    return jsonify(names)


@app.route("/minds/database/<database>", methods=["GET"])
@cross_origin()
@requires_auth
def get_database(database):
    from pymongo import MongoClient

    client = MongoClient(CONFIG.get("mongodb", "uri"))
    db = client["mindsdb"]["databases"].find_one({"dbname": database})

    return jsonify(
        {
            "dbname": db["dbname"],
            "dbtype": db["dbtype"],
            "dbuser": db["dbuser"],
            "dbhost": db["dbhost"],
            "dbport": db["dbport"],
        }
    )


@app.route("/minds/databases", methods=["GET"])
@cross_origin()
@requires_auth
def list_databases():
    import itertools

    from pymongo import MongoClient

    client = MongoClient(CONFIG.get("mongodb", "uri"))
    _databases = [d for d in client["mindsdb"]["databases"].find()]

    counter = itertools.count(0)

    databases = server.list_databases()

    dbs = []
    print(_databases)
    for _db in databases:
        db = next(
            (d for d in _databases if hasattr(d, "dbname") and d.dbname == _db.name),
            None,
        )
        if db is None:
            db = {}
        dbs += [
            {
                "label": _db.name,
                "icon": "las la-database",
                "lazy": True,
                "type": "database",
                "obj": json.dumps(db),
                "id": "db{}".format(next(counter)),
            }
        ]

    return jsonify(dbs)


@app.route("/minds/project/<name>", methods=["POST"])
@cross_origin()
@requires_auth
def create_project(name):
    try:
        server.create_project(name)
        return jsonify({"status": "ok", "message": "Project created successfully!"})
    except Exception as ex:
        status = {"status": "ok", "message": str(ex)}
        return jsonify(status), 500


@app.route("/minds/project", methods=["DELETE"])
@cross_origin()
@requires_auth
def delete_project():
    pass


@app.route("/minds/project/<project>/view/<database>/<view>", methods=["POST"])
@cross_origin()
@requires_auth
def create_view(project, database, view):
    data: Any = request.get_json()

    db = server.get_database(database)
    project = server.get_project(project)
    project.create_view(view, db.query(data["query"]))

    return jsonify({"status": "ok"})


@app.route("/minds/project/<project>/job/<job>", methods=["POST"])
@cross_origin()
@requires_auth
def create_job(project, job):
    data: Any = request.get_json()
    project = server.get_project(project)
    project.create_job(job, data["query"], repeat_str="1 hour")

    return jsonify({"status": "ok"})


@app.route("/minds/project/<project>/model/<model>/train", methods=["POST"])
@cross_origin()
@requires_auth
def train_model(project, model):
    from pymongo import MongoClient

    client = MongoClient(CONFIG.get("mongodb", "uri"))

    data: Any = request.get_json()
    _project = server.get_project(project)

    table = server.get_database(data["database"]).get_table(data["table"])
    _model = _project.get_model(model)
    _model.refresh()

    return jsonify({"status": "ok"})


@app.route("/minds/project/<project>/model/<model>", methods=["POST"])
@cross_origin()
@requires_auth
def create_model(project, model):
    from pymongo import MongoClient

    client = MongoClient(CONFIG.get("mongodb", "uri"))

    data: Any = request.get_json()
    _project = server.get_project(project)

    table = server.get_database(data["database"]).get_table(data["table"])
    _project.create_model(name=model, predict=data["column"], query=table)

    data["name"] = model
    data["project"] = project
    client["mindsdb"]["models"].insert_one(data)
    return jsonify({"status": "ok"})


@app.route("/db/clear", methods=["POST"])
@cross_origin()
@requires_auth
def clear():
    """Clear data from the database table"""

    data: Any = request.get_json()

    table = data["viewtable"]
    database = data["database"]
    url = data["url"]

    conn = get_connection(database, url)

    with conn.connect() as conn_session:
        conn_session.execute(f"DELETE from {table}")
        conn_session.execute("COMMIT")

    return jsonify({"status": "ok"})


@app.route("/db/rows", methods=["POST"])
@cross_origin()
@requires_auth
def rows():
    """Get all the tables for the database info in the POST json"""

    data: Any = request.get_json()

    table = data["viewtable"]
    database = data["database"]
    url = data["url"]

    schemas = get_tables(database, url)
    conn = get_connection(database, url)

    with conn.connect() as conn_session:
        rows = conn_session.execute(f"SELECT * from {table} limit 100")

        results = []
        for schema in schemas:
            if schema["name"] == table:
                for row in rows:
                    results += [{col: data for col, data in zip(schema["cols"], row)}]

    return jsonify(results)


@app.route("/db/inference/rows/<database>/<project>/<model>", methods=["GET"])
@cross_origin()
@requires_auth
def inference_rows(database, project, model):
    """Get all the tables for the database info in the POST json"""
    from pymongo import MongoClient

    client = MongoClient(CONFIG.get("mongodb", "uri"))

    db = client["mindsdb"]["databases"].find_one({"dbname": database})
    _dbmodel = client["mindsdb"]["models"].find_one(
        {"project": project, "database": database, "name": model}
    )

    _project = server.get_project(project)

    _model = _project.get_model(model)

    # Get name of database from mongo, create connection string from stored properties
    # get table cols
    # get rows from mindsdb
    cols = []

    if db["dbtype"] == "Postgres":
        url = f"postgresql://{db['dbuser']}:{db['dbpwd']}@{db['dbhost']}:{db['dbport']}/{db['dbname']}"

        tables = get_tables(db["dbtype"], url)

        cols = [t["cols"] for t in tables if t["name"] == _dbmodel["table"]]
        cols = cols[0]

    return jsonify({"cols": cols, "rows": []})


def get_tables(database, url):

    conn = get_connection(database, url)

    # TODO: Switch to sqlalchemy approach
    tables = conn.table_names()

    results = []

    from pymongo import MongoClient

    client = MongoClient(CONFIG.get("mongodb", "uri"))
    with client:
        with conn.connect() as conn_session:
            ddl = client["elastic"]["schemas"].find_one({"type": database, "url": url})
            for table in tables:
                rows = conn_session.execute(f"select * from {table} limit 1")
                cols = [str(key) for key in rows.keys()]

                results += [
                    {"name": table, "cols": cols, "schema": ddl["schema"].strip()}
                ]

    return results


@app.route("/db/tables", methods=["POST"])
@cross_origin()
@requires_auth
def tables():
    """Get all the tables for the database info in the POST json"""
    data: Any = request.get_json()

    database = data["type"]
    url = data["url"]
    ddl = data["schema"]

    results = get_tables(database, url)

    return jsonify({"status": "ok", "tables": results})


def get_connection(database, url):
    import sqlite3
    from urllib.parse import urlparse

    import sqlalchemy

    if database == "SQLite":
        engine = sqlalchemy.create_engine(url)

        dbname = urlparse(url).path.split("/")[1]
        con = sqlite3.connect(f"{dbname}")
        cur = con.cursor()
        return engine

    if database == "Postgres":
        try:
            engine = sqlalchemy.create_engine(url)
            return engine
        except Exception as ex:
            print(ex)

    return None


@app.route("/db/test", methods=["POST"])
@cross_origin()
@requires_auth
def test():
    """Test database connection"""

    data: Any = request.get_json()

    database = data["type"]
    url = data["url"]

    if get_connection(database, url):

        return jsonify({"status": "ok"})

    return jsonify({"status": "error"}), 500


@app.route("/db/schema", methods=["POST"])
@cross_origin()
@requires_auth
def schema():
    """Create one or more schemas/tables for the provided database info"""
    data: Any = request.get_json()

    database = data["type"]
    url = data["url"]
    ddl = data["schema"].strip()
    logging.info("DDL %s", ddl)

    from pymongo import MongoClient

    client = MongoClient(CONFIG.get("mongodb", "uri"))
    with client:
        client["elastic"]["schemas"].update_one(
            {"type": database, "url": url}, {"$set": data}, upsert=True
        )

        conn = get_connection(database, url)

        with conn.connect() as conn_session:

            stmts = ddl.split(";")

            for stmt in stmts:
                conn_session.execute(stmt)

    return jsonify({"status": "ok"})


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
