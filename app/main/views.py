from . import bp
from flask import render_template

@bp.route('/')
@bp.route('/home')
@bp.route('/index')
def index():
  return render_template('main/home.html', title = 'Página inicial')