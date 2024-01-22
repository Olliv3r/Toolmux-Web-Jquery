from . import bp
from flask import render_template, current_app, request, redirect, url_for, flash, jsonify
from app.models import Tool, Category, TypeInstall
from .forms import ToolAddCreateForm, ToolUpdateCreateForm, ToolSearchCreateForm
from app import db

@bp.route('/tools')
def tools():
  page = request.args.get('page', 1, type = int)
  tools = Tool.query.order_by(Tool.created.desc()).paginate(page = page, per_page = current_app.config['PER_PAGE_TOOLS'], error_out = False)
  
  prev_url = url_for('tool.tools', page = tools.prev_num) if tools.has_prev else None
  next_url = url_for('tool.tools', page = tools.next_num) if tools.has_next else None
  
  return jsonify({'tools_response': render_template('tool/tools.html', title = 'Ferramentas', tools = tools.items, prev_url = prev_url, next_url = next_url)})

@bp.route('/get-data-tc')
def getDataTypesinstallCategories():
  types_install = [{'id': ti.id, 'name': ti.name} for ti in TypeInstall.query.order_by(TypeInstall.id.asc()).all()]
  categories = [{'id': ca.id, 'name': ca.name} for ca in Category.query.order_by(Category.id.asc()).all()]

  return jsonify({
    'types_install': types_install, 
    'categories': categories
  })

@bp.route('/add-tool', methods = ['GET', 'POST'])
def addTool():
  if request.method == 'POST':
    tool = Tool(name = request.form['name'],
      author = request.form['author'],
      alias = request.form['alias'],
      custom_alias = request.form['custom_alias'],
      name_repo = request.form['name_repo'],
      link = request.form['link'],
      type_install = TypeInstall.query.get(request.form['type_install']),
      category = Category.query.get(request.form['category']),
      dependencies = request.form['dependencies'],
      installation_tip = request.form['installation_tip'])
    db.session.add(tool)
    db.session.commit()
  return jsonify(f'Ferramenta adicionada com sucesso!')
  
@bp.route('/view-tool')
def viewTool():
  tool_id = request.args.get('tool_id')
  tool = Tool.query.filter_by(id = tool_id).first()
  if tool is None:
    return jsonify('Ferramenta não existe') 
  return jsonify({'view_tool_response': render_template('tool/view_tool.html', tool = tool)})

@bp.route('/get-data-update')
def getDataUpdate():
  tool = Tool.query.filter_by(id = request.args.get('tool_id')).first()
  if tool is None:
    return jsonify({'msg': 'Ferramenta não foi encontrada!'})
  types_install = [{'id': ti.id, 'name': ti.name} for ti in TypeInstall.query.order_by(TypeInstall.id.asc()).all()]
  categories = [{'id': ca.id, 'name': ca.name} for ca in Category.query.order_by(Category.id.asc()).all()]
  
  return jsonify({
    'id': tool.id,
    'name': tool.name,
    'author': tool.author,
    'alias': tool.alias,
    'custom_alias': tool.custom_alias,
    'name_repo': tool.name_repo,
    'link': tool.link,
    'type_install_id': tool.type_install_id,
    'type_install_name': tool.type_install.name,
    'category_id': tool.category_id,
    'category_name': tool.category.name,
    'dependencies': tool.dependencies,
    'installation_tip': tool.installation_tip,
    'types_install': types_install,
    'categories': categories
  })

@bp.route('/update-tool', methods = ['GET', 'POST'])
def updateTool():
  if request.method == 'POST':
    tool = Tool.query.filter_by(id = request.form['tool_id']).first()
    if tool is None:
      return jsonify({'msg': 'Ferramenta não existe!'})
    tool.name = request.form['name']
    tool.author = request.form['author']
    tool.alias = request.form['alias']
    tool.custom_alias = request.form['custom_alias']
    tool.name_repo = request.form['name_repo']
    tool.link = request.form['link']
    tool.type_install = TypeInstall.query.get(request.form['type_install_id'])
    tool.category = Category.query.get(request.form['category_id'])
    tool.dependencies = request.form['dependencies']
    tool.installation_tip = request.form['installation_tip']
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

@bp.route('/data-search', methods = ['GET', 'POST'])
def dataSearch():
  if request.method == 'POST':
    search_word = request.form['query']

    if search_word == "":
      tools = Tool.query.order_by(Tool.created.desc()).limit(10).all()
    else:
      search_text = "%{}%".format(search_word)
      tools = Tool.query.filter(Tool.name.contains(search_text)).all()
  return jsonify({'responsehtml': render_template('tool/search_response.html', tools = tools, count = len(tools))})