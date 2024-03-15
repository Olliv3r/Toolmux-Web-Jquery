from . import bp
from flask import render_template, request, jsonify

@bp.route('/test')
def test():
  return render_template('test/recort.html', title='Teste')

@bp.route('/save', methods=['POST'])
def save():
  data = request.json
  print(data)
  
  return jsonify({
    'msg': 'Coordenadas salvas!'
  })
