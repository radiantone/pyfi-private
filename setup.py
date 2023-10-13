#!/usr/bin/env python3

import os
import glob
import shutil
from setuptools import setup, Command
import distutils.cmd
import distutils.log
import setuptools
import subprocess

# get key package details from py_pkg/__version__.py
about = {}  # type: ignore
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'pyfi', '__version__.py')) as f:
    exec(f.read(), about)

# load the README file and use it as the long_description for PyPI
with open('README.md', 'r') as f:
    readme = f.read()

class FormatterCommand(distutils.cmd.Command):
    """A custom command to run Pylint on all Python source files."""

    description = 'Run black code formatter'
    user_options = [

    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        command = [
            'black pyfi']

        self.announce(
            'Running command: %s' % str(command),
            level=distutils.log.INFO)
        subprocess.Popen(command, shell=True)


class PyTestCommand(distutils.cmd.Command):
    """A custom command to run Pylint on all Python source files."""

    description = 'Run pytest tests'
    user_options = [

    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        command = [
            'pytest --full-trace --verbose --color=yes --disable-pytest-warnings --no-summary --pyargs pyfi.tests']

        self.announce(
            'Running command: %s' % str(command),
            level=distutils.log.INFO)
        subprocess.Popen(command, shell=True)


class PylintCommand(distutils.cmd.Command):
    """A custom command to run Pylint on all Python source files."""

    description = 'run Pylint on Python source files'
    user_options = [
        # The format is (long option, short option, description).
        ('pylint-rcfile=', None, 'path to Pylint config file'),
    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.pylint_rcfile = ''

    def finalize_options(self):
        """Post-process options."""
        if self.pylint_rcfile:
            assert os.path.exists(self.pylint_rcfile), (
                'Pylint config file %s does not exist.' % self.pylint_rcfile)

    def run(self):
        """Run command."""
        command = ['pylint pyfi']
        self.announce(
            'Running command: %s' % str(command),
            level=distutils.log.INFO)
        subprocess.Popen(command, shell=True)


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    CLEAN_FILES = './celerybeat* ./docs/_build ./*.out ./*.log ./work/* ./build ./dist ./__pycache__ ./*/__pycache__ ./*.pyc ./ssh*py ./*.tgz ./.pytest_cache ./*.egg-info'.split(
        ' ')

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        global here

        for path_spec in self.CLEAN_FILES:
            # Make paths absolute and relative to this path
            abs_paths = glob.glob(os.path.normpath(
                os.path.join(here, path_spec)))
            for path in [str(p) for p in abs_paths]:
                if not path.startswith(here):
                    # Die if path in CLEAN_FILES is absolute + outside this directory
                    raise ValueError(
                        "%s is not a path inside %s" % (path, here))
                print('removing %s' % os.path.relpath(path))
                try:
                    shutil.rmtree(path)
                except:
                    os.remove(path)


# package configuration - for reference see:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#id9
setup(
    name=about['__title__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=['pyfi', 'pyfi.tests', 'pyfi.util', 'pyfi.server', 'pyfi.yaml', 'pyfi.scheduler', 'pyfi.client.user', 'pyfi.config', 'pyfi.client.example', 'pyfi.client.example.api', 'pyfi.client', 'pyfi.api', 'pyfi.api.resource', 'pyfi.api.resource.dto', 'pyfi.server', 'pyfi.worker', 'pyfi.agent',
              'pyfi.blueprints', 'pyfi.util.tasks', 'pyfi.db', 'pyfi.db.postgres', 'pyfi.db.model', 'pyfi.web'],
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        'amqp',
        'celery',
        'click',
        'flask',
        'bjoern',
        'virtualenv-api',
        'redis',
        'flask-restx',
        'prettytable',
        'sqlalchemy',
        'alembic',
        'eventlet',
        'pptree',
        'coloredlogs',
        'gunicorn',
        'paramiko',
        'uvicorn',
        'pyyaml',
        'psutil',
        'setproctitle',
        'requests',
        'humanize',
        'schedule',
        'apscheduler',
        'sphinx',
        'rejson',
        # 'simpy',
        'newrelic',
        'oso',
        'sqlalchemy-oso',
        'pyschedule',
        'uvicorn[standard]',
        'psycopg2',
        'docker'
        # 'sphinx-material @ git+https://github.com/radiantone/sphinx-material'
    ],
    license=about['__license__'],
    zip_safe=False,
    cmdclass={
        'clean': CleanCommand,
        'pylint': PylintCommand,
        'test': PyTestCommand,
        'format': FormatterCommand
    },
    entry_points={
        'console_scripts': ['flow=pyfi.cli:cli']
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='parallel processing, devops, dataflow, supercomputing, workflows'
)
