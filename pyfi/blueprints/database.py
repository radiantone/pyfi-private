import logging
from typing import Any

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

blueprint = Blueprint("database", __name__)
