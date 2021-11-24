import logging
import paramiko

def install_repo(path, hostname, username, sshkey, branch, repo, commit=None):
    _ssh = paramiko.SSHClient()
    _ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    _ssh.connect(hostname=hostname, username=username,
                    key_filename=sshkey)
    command = "mkdir -p {};cd {};git clone -b {} --single-branch {} git".format(path, path, branch, repo.split('#')[0])
    _, stdout, _ = _ssh.exec_command(command)
    for line in stdout.read().splitlines():
        logging.info("SSH: git clone: stdout: %s", line)

    command = "cd {}/git; python3.8 -m venv venv".format(path)
    _, stdout, _ = _ssh.exec_command(command)
    for line in stdout.read().splitlines():
        logging.info("python3 -m venv venv: stdout: %s", line)

    command = "cd {}/git; venv/bin/pip install --upgrade pip".format(path)
    _, stdout, _ = _ssh.exec_command(command)
    for line in stdout.read().splitlines():
        logging.info("pip install --upgrade pip: stdout: %s", line)

    command = "cd {}/git; venv/bin/pip install -e .".format(path)
    _, stdout, _ = _ssh.exec_command(command)
    for line in stdout.read().splitlines():
        logging.info("python setup.py install: stdout: %s", line)

    command = "cd {}/git; venv/bin/python3.8 setup.py install".format(path)
    _, stdout, _ = _ssh.exec_command(command)
    for line in stdout.read().splitlines():
        logging.info("python setup.py install: stdout: %s", line)

    command = "cd {}/git; venv/bin/pyfi agent start --clean -p 1".format(
        path)
    _, stdout, _ = _ssh.exec_command(command)
    for line in stdout.read().splitlines():
        logging.info("agent: stdout: %s", line)

def build_network(detail):
    """ Given a parsed yaml detail, build out the pyfi network"""

    import paramiko

    for nodename in detail['network']['nodes']:
        # For each node, check out repo, build venv
        node = detail['network']['nodes'][nodename]
        logging.info("Deploying node: {}".format(nodename))
        logging.info("Host: {}".format(node['hostname']))
        logging.info("ssh key: {}".format(node['ssh']['key']))
        logging.info("ssh user: {}".format(node['ssh']['user']))
        # Generate, copy pyfi.ini

        for agentname in node['agents']:
            agent = node['agents'][agentname]
            for processorname in agent['processors']:
                processor = agent['processors'][processorname]
                # for each processor, add to database
                logging.info("Creating processor {}".format(processorname))
                install_repo(node['path']+'/'+processorname, node['hostname'],
                             node['ssh']['user'], node['ssh']['key'], "main", processor['gitrepo'])

            logging.info("Starting agent {}".format(agentname))
    # start agent
    logging.info("Built network: {}".format(detail['network']['name']))
