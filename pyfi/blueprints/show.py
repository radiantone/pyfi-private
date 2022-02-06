from flask import Blueprint

blueprint = Blueprint("show", __name__)


@blueprint.route("/show/<page>")
def show(page):
    return "show {}".format(page)


@blueprint.route("/one")
def one():
    return "show one"
