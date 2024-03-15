from . import bp
from flask import render_template, jsonify, request, current_app
import sqlalchemy as sa
from app.models import User, SituationUser, Role, Tool, Category, InstallationType, Author, SituationTool, Comment
from app import db
from app.decorators import admin_required
from datetime import datetime

# Renderiza o painel
@bp.route('/dashboard', methods=['GET'])
def dashboard():
  return render_template('dashboard/dashboard.html', title='Painel de Controle')

# Renderiza conteudo do painel
@bp.route('/get-dashboard-home', methods=['GET'])
def getDashboardHome():
  qtd_users = db.session.scalars(sa.select(User)).all()
  qtd_comments = db.session.scalars(sa.select(Comment)).all()
  return jsonify({'dashboard_home': render_template('dashboard/dashboard_home.html', qtd_users=len(qtd_users), qtd_comments=len(qtd_comments)), 'title': 'Painel'})
  
# Renderiza usuários no painel
@bp.route('/get-dashboard-user', methods=['GET'])
def getDashboardUser():
  query = sa.select(User).order_by(User.created.desc())
  page = request.args.get('page', 1, type=int)
  users = db.paginate(query, page=page, per_page=current_app.config['PER_PAGE_USERS'], error_out=False)
  prev_url = url_for('dashboard.getDashboardUser', page=users.prev_num) if users.has_prev else None
  next_url = url_for('dashboard.getDashboardUser', page=users.next_num) if users.has_next else None
  return jsonify({'dashboard_user': render_template('dashboard/dashboard_user.html', users = users.items, prev_url = prev_url, next_url = next_url), 'title': 'Usuários'})
  
# Renderiza ferramentas no painel
@bp.route('/get-dashboard-tool', methods=['GET'])
def getDashboardTool():
  query = sa.select(Tool).order_by(Tool.created.desc())
  page = request.args.get('page', 1, type=int)
  tools = db.paginate(query, page=page, per_page=current_app.config['PER_PAGE_TOOLS'], error_out=False)
  prev_url = url_for('dashboard.getDashboardTool', page=tools.prev_num) if tools.has_prev else None
  next_url = url_for('dashboard.getDashboardTool', page=tools.next_num) if tools.has_next else None
  return jsonify({'dashboard_tool': render_template('dashboard/dashboard_tool.html', tools = tools.items, prev_url = prev_url, next_url = next_url), 'title': 'Ferramentas'})

# Pega informçôes padrão de Usuário
@bp.route('/get-data-sr')
@admin_required
def getDataSR():
  situationsusers = [{'id': si.id, 'name': si.name} for si in db.session.scalars(sa.select(SituationUser).order_by(SituationUser.id.asc())).all()]
  roles = [{'id': ro.id, 'name': ro.name} for ro in db.session.scalars(sa.select(Role).order_by(Role.id.asc())).all()]
  return jsonify(
    {
      'situationsusers': situationsusers,
      'roles': roles
    }
  )

# Valida e-mail
@bp.route('/validate-email', methods=['POST'])
def validateEmail():
  user = db.session.scalar(sa.select(User).where(User.email == request.form['email']))
  if user is not None:
    return jsonify({'exists': True})
  return jsonify({'exists': False})
  
# Valida username
@bp.route('/validate-username', methods=['POST'])
def validateUsername():
  user = db.session.scalar(sa.select(User).where(User.username == request.form['username']))
  if user is not None:
    return jsonify({'exists': True})
  return jsonify({'exists': False})

# Adiciona um Usuário
@bp.route('/add-user', methods = ['POST'])
@admin_required
def addUser():
  if request.method == 'POST':
    query = sa.select(User)
    if db.session.scalar(query.where(User.username == request.form['username'])) is not None:
      return jsonify({'msg': 'Nome de usuário já está cadastrado!', 'alert': 'alert alert-danger'})
      
    if db.session.scalar(query.where(User.email == request.form['email'])) is not None:
      return jsonify({'msg': 'E-mail já está cadastrado!', 'alert': 'alert alert-danger'})
    
    user = User(
      username = request.form['username'], 
      email = request.form['email'], 
      situationuser = db.session.get(SituationUser, int(request.form['situationuser'])), 
      role = db.session.get(Role, int(request.form['role'])))
    user.confirmed = request.form['confirmed'] == "on"
    user.set_password(request.form['password'])
    db.session.add(user)
    db.session.commit()
  return jsonify({'msg': 'Usuário adicionado com sucesso!', 'alert': 'alert alert-success'})
  
# Visualiza informçôes de um Usuário
@bp.route('/view-user')
@admin_required
def viewUser():
  user_id = request.args.get('user_id')
  user = db.session.scalar(sa.select(User).filter_by(id = user_id))
  if user is None:
    return jsonify({'msg': 'Usuário não existe'})
  return jsonify({
    'view_user_response': render_template('dashboard/view_user.html', user = user)
  })

# Pega dados de um Usuário
@bp.route('/get-data-user')
@admin_required
def getDataEdit():
  situationsusers = [{'id': si.id, 'name': si.name} for si in db.session.scalars(sa.select(SituationUser).order_by(SituationUser.id.asc())).all()]
  roles = [{'id': si.id, 'name': si.name} for si in db.session.scalars(sa.select(Role).order_by(Role.id.asc())).all()]
  user = db.session.scalar(sa.select(User).filter_by(id = request.args.get('user_id')))
  if user is None:
    return jsonify({'msg': 'Usuário não foi encontrada!'})
  else:
    return jsonify({
      'username': user.username,
      'email': user.email,
      'situationsusers': situationsusers,
      'roles': roles,
      'situation_user_id': user.situation_user_id,
      'role_id': user.role_id,
      'confirmed': user.confirmed
    })

# Atualiza dados de um Usuário
@bp.route('/edit-user', methods = ['GET', 'POST'])
@admin_required
def editUser():
  if request.method == 'POST':
    user = db.session.scalar(sa.select(User).filter_by(id = request.form['user_id']))
    if user is None:
      return jsonify({'msg': 'Usuário não existe!'})
    user.username = request.form['username']
    user.email = request.form['email']
    user.situationuser = db.session.get(SituationUser, int(request.form['situationuser']))
    user.role = db.session.get(Role, int(request.form['role']))
    user.confirmed = request.form['confirmed'] == "on"
    user.modified = datetime.utcnow()
    db.session.add(user)
    db.session.commit()
  return jsonify({'msg': 'Usuário atualizado com sucesso'})

# Deleta um Usuário
@bp.route('/delete-user', methods = ['GET', 'POST'])
@admin_required
def deleteUser():
  user = db.session.scalar(sa.select(User).filter_by(id = request.form['user_id']))
  if user is None:
    return jsonify({'msg': 'Usuário não existe!'})
  db.session.delete(user)
  db.session.commit()
  return jsonify({'msg': 'Usuário excluído com sucesso!'})

# Carrega dados pesquisados
"""
@bp.route('/search-users')
@admin_required
def searchUsers():
  search_word = request.args.get('search_text')

  if search_word == "":
    users = db.session.scalars(sa.select(User).order_by(User.created.desc()).limit(10)).all()
  else:
    search_text = f"%{search_word}%"
    users = db.session.scalars(sa.select(User).filter(User.username.ilike(search_text))).all()
  return jsonify({'search_users': render_template('dashboard/search_users.html', users = users, count = len(users))})
"""

# Pega informaçôes: tipos de instalação e categorias
@bp.route('/get-data-ics')
@admin_required
def getDataICS():
  installation_types = [{'id': it.id, 'name': it.name} for it in InstallationType.query.order_by(InstallationType.id.asc()).all()]
  categories = [{'id': ca.id, 'name': ca.name} for ca in Category.query.order_by(Category.id.asc()).all()]
  situations = [{'id': si.id, 'name': si.name} for si in SituationTool.query.order_by(SituationTool.id.asc()).all()]

  return jsonify({
    'installation_types': installation_types,
    'categories': categories,
    'situations': situations,
  })

# Adiciona uma ferramenta
@bp.route('/add-tool', methods = ['POST'])
@admin_required
def addTool():
  if request.method == 'POST':
    tool = Tool(
      name = request.form['name'], 
      tool_author = Author(name = request.form['author']),
      alias = request.form['alias'],
      executable = request.form['executable'],
      link = request.form['link'],
      installation_type = InstallationType.query.get(request.form['installation_type_id']),
      category = Category.query.get(request.form['category_id']),
      situationtool = SituationTool.query.get(request.form['situation_id']),
      dependencies = request.form['dependencies'],
      installation_tip = request.form['installation_tip'],
      description = request.form['description'])
  
    if tool.link != "":
      tool.name_repo = tool.link[19:].split('/')[1]
      tool.author.github = tool.link[:19] + tool.link[19:].split('/')[0]
    db.session.add(tool)
    db.session.commit()
  return jsonify({'msg': 'Ferramenta adicionada com sucesso!'})

# Visualiza uma ferramenta
@bp.route('/view-tool')
@admin_required
def viewTool():
  tool_id = request.args.get('tool_id')
  tool = Tool.query.filter_by(id = tool_id).first()
  if tool is None:
    return jsonify({'msg': 'Ferramenta não existe'})
  return jsonify({'view_tool_response': render_template('dashboard/view_tool.html', tool = tool)})

# Pega informaçôes de uma ferramenta
@bp.route('/get-data-tool')
@admin_required
def getDataTool():
  tool = Tool.query.filter_by(id = request.args.get('tool_id')).first()
  if tool is None:
    return jsonify({'msg': 'Ferramenta não foi encontrada!'})
  installation_types = [{'id': it.id, 'name': it.name} for it in InstallationType.query.order_by(InstallationType.id.asc()).all()]
  categories = [{'id': ca.id, 'name': ca.name} for ca in Category.query.order_by(Category.id.asc()).all()]
  situations = [{'id': si.id, 'name': si.name} for si in SituationTool.query.order_by(SituationTool.id.asc()).all()]
  
  return jsonify({
    'id': tool.id,
    'name': tool.name,
    'author': tool.tool_author.name,
    'alias': tool.alias,
    'executable': tool.executable,
    'name_repo': tool.name_repo,
    'link': tool.link,
    'installation_type_id': tool.installation_type_id,
    'category_id': tool.category_id,
    'situation_id': tool.situation_tool_id,
    'dependencies': tool.dependencies,
    'installation_tip': tool.installation_tip,
    'description': tool.description,
    'installation_types': installation_types,
    'categories': categories,
    'situations': situations
  })

# Edita uma ferramenta
@bp.route('/edit-tool', methods = ['GET', 'POST'])
@admin_required
def editTool():
  if request.method == 'POST':
    tool = Tool.query.filter_by(id = request.form['tool_id']).first()
    if tool is None:
      return jsonify({'msg': 'Ferramenta não existe!'})
    tool.name = request.form['name']
    tool.tool_author = Author(name = request.form['author'])
    tool.alias = request.form['alias']
    tool.executable = request.form['executable']
    tool.link = request.form['link']
    tool.installation_type = InstallationType.query.get(request.form['installation_type_id'])
    tool.category = Category.query.get(request.form['category_id'])
    tool.situationtool = SituationTool.query.get(request.form['situation_id'])
    tool.dependencies = request.form['dependencies']
    tool.installation_tip = request.form['installation_tip']
    tool.description = request.form['description']
    
    if tool.link != "":
      tool.name_repo = tool.link[19:].split('/')[1]
      tool.author.github = tool.link[:19] + tool.link[19:].split('/')[0]
    tool.modified = datetime.utcnow()
    db.session.add(tool)
    db.session.commit()
  return jsonify({'msg': 'Ferramenta atualizada com sucesso'})

# Deleta uma ferramenta
@bp.route('/delete-tool', methods = ['GET', 'POST'])
@admin_required
def deleteTool():
  tool = Tool.query.filter_by(id = request.form['tool_id']).first()
  if tool is None:
    return jsonify({'msg': 'Ferramenta não existe!'})
  db.session.delete(tool)
  db.session.commit()
  return jsonify({'msg': 'Ferramenta excluída com sucesso!'})

# Pesquisa ferramentas
"""
@bp.route('/search-tools')
@admin_required
def searchTools():
  search_word = request.args.get('search_text')

  if search_word == "":
    tools = Tool.query.order_by(Tool.created.desc()).limit(10).all()
  else:
    search_text = f"%{search_word}%"
    tools = Tool.query.filter(Tool.name.ilike(search_text)).all()
    
  return jsonify({'search_tools': render_template('dashboard/search_tools.html', tools = tools, count = len(tools))})
"""