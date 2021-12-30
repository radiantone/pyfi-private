import logging
import os
import platform

import paramiko
from sqlalchemy import exc as sa_exc

from pyfi.client.api import Node, Processor, Socket, Plug, Agent, Argument, Worker
from pyfi.client.user import USER

HOSTNAME = platform.node()

if 'PYFI_HOSTNAME' in os.environ:
    HOSTNAME = os.environ['PYFI_HOSTNAME']


def remove_network(_ssh, path, ini, polar, hostname, username, sshkey, branch, pyfi, repo, clean, commit=None):
    """ Remote host only needs to have ssh key trust to be managed by pyfi 
        PYFI will remote install itself and manage the running agent processes on it.
        It uses an isolated virtualenvironment for itself AND the processor code, meaning that 
        both use their own virtual environments and do not pollute the host environment.
    """
    if not clean:
        raise

    if _ssh is None:
        _ssh = paramiko.SSHClient()
        _ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _ssh.connect(hostname=hostname, username=username,
                     key_filename=sshkey)

    if hostname != HOSTNAME:
        sftp = _ssh.open_sftp()
        sftp.put(ini, '/home/' + username + '/pyfi.ini')
        sftp.put(polar, '/home/' + username + '/pyfi.polar')

    agent = Agent.find(name=hostname + '.agent')

    # Kill any existing agent
    if agent and agent.pid:
        command = 'kill -s SIGINT ' + str(agent.pid)
        _, stdout, stderr = _ssh.exec_command(command)

    # Kill existing processors and remove existing directories
    # ps -ef|grep pyfi|awk '{ print "kill "$2 }'|sh
    command = "ps -ef|grep 'pyfi worker'|awk '{print \"kill \"$2}'|sh"
    logging.info(hostname + ":" + command)
    _, stdout, stderr = _ssh.exec_command(command)
    for line in stdout.read().splitlines():
        logging.info(hostname + command + ": stdout: % s", line)

    command = "ps -ef|grep pyfi|grep -v 'pyfi compose'|grep -v postgres|awk '{print \"kill \"$2}'|sh"
    logging.info(hostname + ":" + command)
    _, stdout, stderr = _ssh.exec_command(command)
    for line in stdout.read().splitlines():
        logging.info(hostname + command + ": stdout: % s", line)

    command = "ps -ef|grep celery|awk '{print \"kill -9 \"$2}'|sh"
    logging.info(hostname + ":" + command)
    _, stdout, stderr = _ssh.exec_command(command)
    for line in stderr.read().splitlines():
        logging.info(hostname + ":ERROR: % s", line)

    # Remove existing git repos
    _login = repo.split("/", 3)[:3]
    login = _login[0] + "//" + _login[2]
    logging.info("Removing existing install....{}".format(path))
    logging.info("rm -rf {}".format(path))
    _, stdout, stderr = _ssh.exec_command("rm -rf {}".format(path))
    for line in stdout.read().splitlines():
        logging.info(hostname + ":rm -rf %s: git clone: stdout: % s", path, line)

    logging.info("Done")

    return login, _ssh


def install_repo(_ssh, path, ini, polar, hostname, username, sshkey, branch, pyfi, repo, clean, commit=None):
    """ Remote host only needs to have ssh key trust to be managed by pyfi 
        PYFI will remote install itself and manage the running agent processes on it.
        It uses an isolated virtualenvironment for itself AND the processor code, meaning that 
        both use their own virtual environments and do not pollute the host environment.
    """

    _login = repo.split("/", 3)[:3]
    login = _login[0] + "//" + _login[2]

    if _ssh is None:
        try:
            _ssh = paramiko.SSHClient()
            _ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            _ssh.connect(hostname=hostname, username=username,
                         key_filename=sshkey)
        except:
            logging.error("Unable to establish ssh to %s", hostname)
            return

    try:

        # login, _ssh = remove_network(_ssh, path, ini, polar, hostname, username,
        #            sshkey, branch, pyfi, repo, False, commit=None)

        # Install new git repos
        command = "mkdir -p {};cd {};rm -rf git 2> /dev/null; git clone -b {} --single-branch {} git".format(
            path, path, branch, repo.split('#')[0])
        logging.info(hostname + ":" + command)
        _, stdout, stderr = _ssh.exec_command(command)
        for line in stdout.read().splitlines():
            logging.info(hostname + ":" + "SSH: git clone: stdout: %s", line)
        for line in stderr.read().splitlines():
            logging.info(hostname + ":ERROR: % s", line)

        # Create virutal environment
        command = "cd {}/git; python3.9 -m venv venv".format(path)
        logging.info(hostname + ":" + command)
        _, stdout, stderr = _ssh.exec_command(command)
        for line in stdout.read().splitlines():
            logging.info(hostname + ":" + "python3.9 -m venv venv: stdout: %s", line)
        for line in stderr.read().splitlines():
            logging.info(hostname + ":ERROR: % s", line)

        # Upgrade pip
        command = "cd {}/git; venv/bin/pip install --upgrade pip".format(path)
        logging.info(hostname + ":" + command)
        _, stdout, stderr = _ssh.exec_command(command)
        for line in stdout.read().splitlines():
            logging.info(
                hostname + ":" + "pip install --upgrade pip: stdout: %s", line)
        for line in stderr.read().splitlines():
            logging.info(hostname + ":ERROR: % s", line)

        # Install the processor git repo
        command = "cd {}/git; venv/bin/pip install -e .".format(path)
        logging.info(hostname + ":" + command)
        _, stdout, stderr = _ssh.exec_command(command)
        for line in stdout.read().splitlines():
            logging.info(hostname + ":" + command + ": stdout: %s", line)
        for line in stderr.read().splitlines():
            logging.info(hostname + ":ERROR: % s", line)

        command = "cd {}/git; venv/bin/python setup.py install".format(path)
        logging.info(hostname + ":" + command)
        _, stdout, stderr = _ssh.exec_command(command)
        for line in stdout.read().splitlines():
            logging.info(hostname + ":" + command +
                         ": stdout: %s", line)

        # Install pyfi
        command = "cd {}/git; venv/bin/pip install -e git+{}".format(path, pyfi)
        logging.info(hostname + ":" + command)
        _, stdout, stderr = _ssh.exec_command(command)
        for line in stdout.read().splitlines():
            logging.info(hostname + ":" + command + ": stdout: %s", line)
        for line in stderr.read().splitlines():
            logging.info(hostname + ":ERROR: % s", line)

        for line in stderr.read().splitlines():
            logging.info(hostname + ":ERROR: % s", line)
    except:
        logging.info("Skipping uninstall...")

    # Start the agent
    command = "cd {}/git; export GIT_LOGIN={}; venv/bin/pyfi agent start --clean -p 1 >> agent.log 2>&1 &".format(
        path, login)
    _, stdout, stderr = _ssh.exec_command(command)
    logging.info(hostname + ":" + command)
    for line in stdout.read().splitlines():
        logging.info(hostname + ":agent: stdout: %s", line)

    for line in stderr.read().splitlines():
        logging.info(hostname + ":ERROR: % s", line)


def stop_network(detail):
    for nodename in detail['network']['nodes']:
        # For each node, check out repo, build venv
        node = detail['network']['nodes'][nodename]
        if 'enabled' in node and not node['enabled']:
            continue

    pass


def compose_agent(node, agent, deploy, _agent):
    repos = []
    sockets = {}

    for processorname in agent['processors']:
        # for each processor, add to database
        logging.info("Creating processor {}".format(processorname))
        processor = agent['processors'][processorname]
        _processor = Processor(name=processorname, hostname=node['hostname'], beat=processor['beat'], user=USER,
                                module=processor['module'], branch=processor['branch'],
                                concurrency=processor['workers'], agent=_agent.agent,
                                gitrepo=processor['gitrepo'])


        if 'container_image' in processor:
            _processor.processor.container_image = processor['container_image']
            if 'detached' in processor:
                _processor.processor.detached = processor['detached']

            if 'container_version' in processor:
                _processor.processor.container_version = processor['container_version']
            
            if 'use_container' in processor:
                _processor.processor.use_container = processor['use_container']
                

        # if "remove", then delete _processor
        if 'sockets' in processor:
            for socketname in processor['sockets']:
                logging.info("Creating socket {}".format(socketname))
                socket = processor['sockets'][socketname]
                interval = socket['interval'] if 'interval' in socket else -1
                if 'arguments' in socket['task']['function']:
                    arguments = socket['task']['function']
                else:
                    arguments = False
                _socket = Socket(name=socketname, user=USER, interval=interval, processor=_processor, queue={
                    'name': socket['queue']['name']}, task=socket['task']['function']['name'], arguments=arguments)

                sockets[socketname] = _socket

        if 'build' in agent and agent['build'] == False:
            continue

        clean = node['clean'] if 'clean' in node else True
        deploy = node['deploy'] if 'deploy' in node else deploy

        repos += [(deploy, (None, node['path'] + '/' + processorname, node['ini'], node['polar'], node['hostname'],
                    node['ssh']['user'], node['ssh']['key'], "main", processor['pyfirepo'], processor['gitrepo'],
                    clean))]

    return repos, sockets


def compose_network(detail, command="build", deploy=True, nodes=[]):
    """ Given a parsed yaml detail, build out the pyfi network"""

    sockets = {}
    repos = []

    for nodename in detail['network']['nodes']:
        node = detail['network']['nodes'][nodename]
        node['name'] = nodename

    _nodes = [detail['network']['nodes'][nodename]
              for nodename in nodes] if len(nodes) > 0 else [detail['network']['nodes'][nodename]
                                          for nodename in detail['network']['nodes']]

    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)

        for node in _nodes:
            nodename = node['name']
            # For each node, check out repo, build venv
            _node = Node(name=nodename, hostname=node['hostname'])

            if 'enabled' in node and not node['enabled']:
                continue

            logging.info("Deploying node: {}".format(nodename))
            logging.info("Host: {}".format(node['hostname']))
            logging.info("ssh key: {}".format(node['ssh']['key']))
            logging.info("ssh user: {}".format(node['ssh']['user']))
            # Generate, copy pyfi.ini

            for agentname in node['agents']:
                agent = node['agents'][agentname]
                logging.info(
                    "Creating agent %s ", node['hostname'] + ".agent")
                _agent = Agent(hostname=node['hostname'], node=_node,
                                name=node['hostname'] + ".agent")
                _node.node.agent = _agent.agent
                _repos, _sockets = compose_agent(node, agent, deploy, _agent)

                _node.session.add(_agent.agent)
                for socketname in _sockets:
                    socket = _sockets[socketname]
                    _node.session.add(socket.socket)
                    _node.session.add(socket.processor.processor)
                    logging.info(
                        "Creating worker %s ", node['hostname'] + ".agent."+socket.socket.processor.name+".worker")
                    worker = Worker(
                        hostname=node['hostname'], agent=_agent.agent, name=node['hostname'] + ".agent."+socket.socket.processor.name+".worker")
                    logging.info("Worker ID %s", worker.worker.id)
                    _agent.agent.workers  += [worker.worker]
                    worker.worker.processor = socket.processor.processor

                repos += _repos
                sockets.update(_sockets)
                _node.session.add(worker.worker)
                _node.session.add(_node.node)
                _node.session.commit()

    if 'plugs' in detail['network']:
        for plugname in detail['network']['plugs']:
            plug = detail['network']['plugs'][plugname]

            if hasattr(plug, 'enabled') and plug.enabled == False:
                continue

            plug_queue = plug['queue']
            argument = plug['argument'] if 'argument' in plug else None
            source = plug['source']
            target = plug['target']

            source_socket = sockets[source]
            target_socket = sockets[target]

            _plug = Plug(name=plugname, processor=source_socket.processor, user=USER,
                         source=source_socket, queue=plug_queue, target=target_socket)
            _plug.session.add(target_socket.task)
            if argument:
                logging.info("Fetching argument %s",argument)
                _argument = Argument.find(argument, target_socket.task.name)
                logging.info("Found argument: %s",_argument.name)
                if _argument is None:
                    logging.error("No argument %s exists. Please create arguments for task.",argument)

                # attach argument to plug
                _plug.session.add(_argument)
                _plug.argument_id = _argument.id
                _argument.plugs += [_plug.plug]
            
            _plug.session.commit()

            logging.info("Created plug: %s", _plug)

    for repo in repos:
        deploy = repo[0]

        if command == "build":
            if deploy:
                logging.info("Installing repo %s", repo)
                install_repo(*repo[1])
        elif command == "remove":
            try:
                remove_network(*repo)
            except:
                pass

    # start agent
    logging.info("Built network: {}".format(detail['network']['name']))
