from flask import Blueprint

bp = Blueprint("test", __name__)

from . import views