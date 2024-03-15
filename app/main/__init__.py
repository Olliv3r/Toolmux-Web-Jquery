from flask import Blueprint
from app.models import Permission

bp = Blueprint('main', __name__)

from . import views

@bp.app_context_processor
def inject_permissions():
  return dict(Permission=Permission)