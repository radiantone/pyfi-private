import logging
import paramiko
import platform

from pyfi.client.api import Processor, Socket, Plug
from pyfi.config import CONFIG
from pyfi.client.user import USER

HOSTNAME = platform.node()

def install_repo(path, ini, polar, hostname, username, sshkey, branch, pyfi, repo, commit=None):
    _ssh = paramiko.SSHClient()
    _ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    _ssh.connect(hostname=hostname, username=username,
                    key_filename=sshkey)

    if hostname != HOSTNAME:
        sftp = _ssh.open_sftp()
        sftp.put(ini, '/home/'+username+'/pyfi.ini')
        sftp.put(polar, '/home/'+username+'/pyfi.polar')


    # Kill existing processors and remove existing directories
    # ps -ef|grep pyfi|awk '{ print "kill "$2 }'|sh
    command = "ps -ef|grep pyfi|awk '{print \"kill \"$2}'|sh"
    logging.info(hostname+":"+command)
    _, stdout, stderr = _ssh.exec_command(command)
    command = "ps -ef|grep celery|awk '{print \"kill \"$2}'|sh"
    logging.info(hostname+":"+command)
    _, stdout, stderr = _ssh.exec_command(command)
    for line in stdout.read().splitlines():
        logging.info(hostname+":SSH: git clone: stdout: % s", line)
    for line in stderr.read().splitlines():
        logging.info(hostname+":ERROR: % s", line)

    _login = repo.split("/", 3)[:3]
    login = _login[0]+"//"+_login[2]
    logging.info("Removing existing install....{}".format(path))
    logging.info("rm -rf {}".format(path))
    _, stdout, stderr = _ssh.exec_command("rm -rf {}".format(path))
    for line in stdout.read().splitlines():
        logging.info(hostname+":rm -rf %s: git clone: stdout: % s", path, line)

    logging.info("Done")
    
    command = "mkdir -p {};cd {};rm -rf git 2> /dev/null; git clone -b {} --single-branch {} git".format(
        path, path, branch, repo.split('#')[0])
    logging.info(hostname+":"+command)
    _, stdout, stderr = _ssh.exec_command(command)
    for line in stdout.read().splitlines():
        logging.info(hostname+":"+"SSH: git clone: stdout: %s", line)
    for line in stderr.read().splitlines():
        logging.info(hostname+":ERROR: % s", line)

    command = "cd {}/git; python3.9 -m venv venv".format(path)
    logging.info(hostname+":"+command)
    _, stdout, stderr = _ssh.exec_command(command)
    for line in stdout.read().splitlines():
        logging.info(hostname+":"+"python3.9 -m venv venv: stdout: %s", line)
    for line in stderr.read().splitlines():
        logging.info(hostname+":ERROR: % s", line)

    command = "cd {}/git; venv/bin/pip install --upgrade pip".format(path)
    logging.info(hostname+":"+command)
    _, stdout, stderr = _ssh.exec_command(command)
    for line in stdout.read().splitlines():
        logging.info(
            hostname+":"+"pip install --upgrade pip: stdout: %s", line)
    for line in stderr.read().splitlines():
        logging.info(hostname+":ERROR: % s", line)

    command = "cd {}/git; venv/bin/pip install -e .".format(path)
    logging.info(hostname+":"+command)
    _, stdout, stderr = _ssh.exec_command(command)
    for line in stdout.read().splitlines():
        logging.info(hostname+":"+command+": stdout: %s", line)
    for line in stderr.read().splitlines():
        logging.info(hostname+":ERROR: % s", line)

    command = "cd {}/git; venv/bin/pip install -e git+{}".format(path, pyfi)
    logging.info(hostname+":"+command)
    _, stdout, stderr = _ssh.exec_command(command)
    for line in stdout.read().splitlines():
        logging.info(hostname+":"+command+": stdout: %s", line)
    for line in stderr.read().splitlines():
        logging.info(hostname+":ERROR: % s", line)
        
    command = "cd {}/git; venv/bin/python setup.py install".format(path)
    logging.info(hostname+":"+command)
    _, stdout, stderr = _ssh.exec_command(command)
    for line in stdout.read().splitlines():
        logging.info(hostname+":"+command +
                     ": stdout: %s", line)

    for line in stderr.read().splitlines():
        logging.info(hostname+":ERROR: % s", line)

    command = "cd {}/git; export GIT_LOGIN={}; venv/bin/pyfi agent start --clean -p 1 >> agent.log 2>&1 &".format(
        path, login)
    _, stdout, stderr = _ssh.exec_command(command)
    logging.info(hostname+":"+command)
    for line in stdout.read().splitlines():
        logging.info(hostname+":agent: stdout: %s", line)

    for line in stderr.read().splitlines():
        logging.info(hostname+":ERROR: % s", line)

def build_network(detail):
    """ Given a parsed yaml detail, build out the pyfi network"""

    import paramiko

    for nodename in detail['network']['nodes']:
        # For each node, check out repo, build venv
        node = detail['network']['nodes'][nodename]
        if 'enabled' in node and not node['enabled']:
            continue

        logging.info("Deploying node: {}".format(nodename))
        logging.info("Host: {}".format(node['hostname']))
        logging.info("ssh key: {}".format(node['ssh']['key']))
        logging.info("ssh user: {}".format(node['ssh']['user']))
        # Generate, copy pyfi.ini

        for agentname in node['agents']:
            agent = node['agents'][agentname]
            for processorname in agent['processors']:
                # for each processor, add to database
                logging.info("Creating processor {}".format(processorname))
                processor = agent['processors'][processorname]
                _processor = Processor(name=processorname, hostname=node['hostname'], beat=processor['beat'], user=USER, module=processor['module'], branch=processor['branch'], concurrency=processor['workers'],
                                      gitrepo=processor['gitrepo'])

                for socketname in processor['sockets']:
                    logging.info("Creating socket {}".format(socketname))
                    socket = processor['sockets'][socketname]

                    _socket = Socket(name=socketname, user=USER, processor=_processor, queue={
                           'name': socket['queue']['name']}, task=socket['task']['function'])

                logging.info("Installing repository {}".format(
                    processor['gitrepo']))
                install_repo(node['path']+'/'+processorname, node['ini'], node['polar'], node['hostname'],
                             node['ssh']['user'], node['ssh']['key'], "main", processor['pyfirepo'], processor['gitrepo'])

            logging.info("Starting agent {}".format(agentname))
    # start agent
    logging.info("Built network: {}".format(detail['network']['name']))
