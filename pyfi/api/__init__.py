"""
api.py - classes used for remote administration of PYFI network by applications
Implementation of basic UI use cases etc. Login, rename, save/edit/delete, etc
"""
from flask import Blueprint
from flask_restx import Api

from pyfi.api.resource.user import api as user_ns

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="FLASK RESTPLUS API BOILER-PLATE WITH JWT",
    version="1.0",
    description="a boilerplate for flask restplus web service",
)

api.add_namespace(user_ns, path="/user")
