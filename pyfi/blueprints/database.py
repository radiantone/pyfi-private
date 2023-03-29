import logging
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from typing import Any

blueprint = Blueprint("database", __name__)



