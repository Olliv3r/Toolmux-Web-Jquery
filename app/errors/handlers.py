from . import bp
from flask import render_template
from app import db

@bp.app_errorhandler(404)
def not_found_error(error):
  return render_template('errors/404.html', title = 'Página não encontrada!'), 404
  
@bp.app_errorhandler(403)
def forbidden_error(error):
  return render_template('errors/403.html', title = 'Não tem permissão para acessar!'), 404

@bp.app_errorhandler(500)
def internal_error(error):
  db.session.rollback()
  return render_template('errors/500.html', title = 'Problema com o servidor!'), 500

