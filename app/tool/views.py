
from . import bp
from flask import render_template, current_app, request, redirect, url_for, flash, jsonify
from app.models import Tool, Category, InstallationType, Author, Situation
from .forms import ToolAddCreateForm, ToolUpdateCreateForm, ToolSearchCreateForm
from app import db
from sqlalchemy import or_

@bp.route('/tools')
def tools():
  page = request.args.get('page', 1, type = int)
  tools = Tool.query.order_by(Tool.created.desc()).paginate(page = page, per_page = current_app.config['PER_PAGE_TOOLS'], error_out = False)
  
  prev_url = url_for('tool.tools', page = tools.prev_num) if tools.has_prev else None
  next_url = url_for('tool.tools', page = tools.next_num) if tools.has_next else None
  
  return jsonify({'tools': render_template('tool/tools.html', title = 'Ferramentas', tools = tools.items, prev_url = prev_url, next_url = next_url)})

@bp.route('/get-data-ics')
def getDataICS():
  installation_types = [{'id': it.id, 'name': it.name} for it in InstallationType.query.order_by(InstallationType.id.asc()).all()]
  categories = [{'id': ca.id, 'name': ca.name} for ca in Category.query.order_by(Category.id.asc()).all()]
  situations = [{'id': si.id, 'name': si.name} for si in Situation.query.order_by(Situation.id.asc()).all()]

  return jsonify({
    'installation_types': installation_types,
    'categories': categories,
    'situations': situations,
  })

@bp.route('/add-tool', methods = ['POST'])
def addTool():
  if request.method == 'POST':
    data = request.form.to_dict()
    
    tool = Tool(
      name = data['name'],
      author = Author(name = data['author']),
      alias = data['alias'],
      executable = data['executable'],
      link = data['link'],
      installation_type = InstallationType.query.get(data['installation_type']),
      category = Category.query.get(data['category']),
      situation = Situation.query.get(data['situation']),
      dependencies = data['dependencies'],
      installation_tip = data['installation_tip'],
      description = data['description'])
  
    if tool.link != "":
      tool.name_repo = tool.link[19:].split('/')[1]
      tool.author.github = tool.link[:19] + tool.link[19:].split('/')[0]
    db.session.add(tool)
    db.session.commit()
  return jsonify({'msg': 'Ferramenta adicionada com sucesso!'})
  
@bp.route('/view-tool')
def viewTool():
  tool_id = request.args.get('tool_id')
  tool = Tool.query.filter_by(id = tool_id).first()
  if tool is None:
    return jsonify({'msg': 'Ferramenta não existe'})
  return jsonify({'view_tool_response': render_template('tool/view_tool.html', tool = tool)})

@bp.route('/get-data-edit')
def getDataEdit():
  tool = Tool.query.filter_by(id = request.args.get('tool_id')).first()
  if tool is None:
    return jsonify({'msg': 'Ferramenta não foi encontrada!'})
  installation_types = [{'id': it.id, 'name': it.name} for it in InstallationType.query.order_by(InstallationType.id.asc()).all()]
  categories = [{'id': ca.id, 'name': ca.name} for ca in Category.query.order_by(Category.id.asc()).all()]
  situations = [{'id': si.id, 'name': si.name} for si in Situation.query.order_by(Situation.id.asc()).all()]
  
  return jsonify({
    'id': tool.id,
    'name': tool.name,
    'author': tool.author.name,
    'alias': tool.alias,
    'executable': tool.executable,
    'name_repo': tool.name_repo,
    'link': tool.link,
    'installation_type_id': tool.installation_type_id,
    'category_id': tool.category_id,
    'situation_id': tool.situation_id,
    'dependencies': tool.dependencies,
    'installation_tip': tool.installation_tip,
    'description': tool.description,
    'installation_types': installation_types,
    'categories': categories,
    'situations': situations
  })

@bp.route('/edit-tool', methods = ['GET', 'POST'])
def editTool():
  if request.method == 'POST':
    tool = Tool.query.filter_by(id = request.form['tool_id']).first()
    if tool is None:
      return jsonify({'msg': 'Ferramenta não existe!'})
    tool.name = request.form['name']
    tool.author = Author(name = request.form['author'])
    tool.alias = request.form['alias']
    tool.executable = request.form['executable']
    tool.link = request.form['link']
    tool.installation_type = InstallationType.query.get(request.form['installation_type_id'])
    tool.category = Category.query.get(request.form['category_id'])
    tool.situation = Situation.query.get(request.form['situation_id'])
    tool.dependencies = request.form['dependencies']
    tool.installation_tip = request.form['installation_tip']
    tool.description = request.form['description']
    
    if tool.link != "":
      tool.name_repo = tool.link[19:].split('/')[1]
      tool.author.github = tool.link[:19] + tool.link[19:].split('/')[0]
      
    db.session.add(tool)
    db.session.commit()
  return jsonify({'msg': 'Ferramenta atualizada com sucesso'})
  
@bp.route('/delete-tool', methods = ['GET', 'POST'])
def deleteTool():
  tool = Tool.query.filter_by(id = request.form['tool_id']).first()
  if tool is None:
    return jsonify({'msg': 'Ferramenta não existe!'})
  db.session.delete(tool)
  db.session.commit()
  return jsonify({'msg': 'Ferramenta excluída com sucesso!'})

@bp.route('/search')
def search():
  form = ToolSearchCreateForm()
  return render_template('main/search.html', title = 'Pesquisar', form = form)

@bp.route('/search-tools')
def searchTools():
  search_word = request.args.get('keyword')

  if search_word == "":
    tools = Tool.query.order_by(Tool.created.desc()).limit(10).all()
  else:
    search_text = f"%{search_word}%"
    tools = Tool.query.filter(Tool.name.ilike(search_text)).all()
    
  return jsonify({'search_tools': render_template('tool/search_tools.html', tools = tools, count = len(tools))})
