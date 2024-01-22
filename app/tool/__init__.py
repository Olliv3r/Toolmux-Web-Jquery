from flask import Blueprint

bp = Blueprint('tool', __name__)

from . import views