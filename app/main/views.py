from app import db
from . import bp
from app.models import User, Message, Notification, Comment
from app.decorators import admin_required
from flask import render_template, current_app, request ,redirect, url_for, flash, jsonify, send_file, abort
from flask_login import current_user
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
import sqlalchemy as sa
import os
import imghdr

# Home
@bp.route('/index')
@bp.route('/home')
@bp.route('/')
def index():
  return render_template('main/home.html', title = 'Página inicial')

# Trazer imagem de avatar
@bp.route('/get-image', methods=['GET'])
def get_image():
  user_id = request.args.get('user_id')
  user = db.session.scalar(sa.select(User).where(User.id == user_id))
  if user is None:
    return jsonify({'msg': 'Usuário não existe!', 'process': False})

  image_url = user.profile_image_url
  if image_url is None:
    return jsonify({'msg': 'Imagem não existe', 'process': False})
  return jsonify({'image_url': image_url, 'process': True})

# Criar pasta do usuário e remove as imagens caso existam
def create_dir_user(user_id):
  dir_user = os.path.join(current_app.config['UPLOAD_PATH'], str(user_id))
  
  if not os.path.exists(dir_user):
    os.makedirs(dir_user, exist_ok = True)
  else:
    for image in os.listdir(dir_user):
      os.remove(dir_user +'/'+ image)
  return dir_user

# Valida imagem
def validate_image(stream):
  header = stream.read(512)
  stream.seek(0)
  image_format = imghdr.what(None, header)
  
  if not image_format:
    return None
  return '.' + (image_format if image_format != 'jpeg' else 'jpg')
 
# Envia foto de perfil 
@bp.route('/upload', methods=['POST'])
def upload_file():
  uploaded_file = request.files['fileInput']
  
  if uploaded_file.filename != '':
    file_ext = os.path.splitext(uploaded_file.filename)[1]
    
    if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] or \
    file_ext != validate_image(uploaded_file.stream):
      return jsonify({'msg': 'Formato de imagem inválido!', 'status': '400'})
      
    user_id = request.form['user_id']
    user = db.session.scalar(sa.select(User).where(User.id == user_id))
    
    if user:
      dir_user = create_dir_user(user_id)
      user_folder = os.path.join(current_app.static_folder, 'images', 'avatars', str(user_id))
      filename = secure_filename(uploaded_file.filename)
      image_url = url_for('static', filename="images/avatars/{}/{}".format(user_id, filename))
      uploaded_file.save(os.path.join(dir_user, filename))
      user.profile_image_url = image_url
      db.session.commit()
      return jsonify({'msg': 'Imagem enviada com sucesso'})
    else:
      return jsonify({'msg': 'Imagem não pode ser salva!'})
    
# Renderiza a página de perfil do usuário atualmente logado
@bp.route('/profile', methods=['GET'])
def profile():
  if not current_user.is_authenticated:
    return redirect(url_for('auth.signin', next = url_for('user.profile')))
  return render_template('main/profile.html', title = 'Perfil', user=current_user)

# Carrega dados do usuário atualmente logado na página de perfil
@bp.route('/get-profile', methods=['GET'])
def get_profile():
  return jsonify({'profile': render_template('main/user_profile.html', user=current_user)})
  
# Atualiza os dados do usuário atualmente logado
@bp.route('/edit-profile-user', methods=['POST'])
def edit_profile_user():
  if request.method == 'POST':
    user = db.session.scalar(sa.select(User).where(User.username == request.form['username']))
    if user is not None:
      user.name = request.form['name']
      user.email = request.form['email']
      user.website = request.form['website']
      user.profission = request.form['profission']
      user.address = request.form['address']
      user.github = request.form['github']
      db.session.commit()
      return jsonify({'msg': 'Perfil atualizado com sucesso!'})
    else:
      return jsonify({'msg': 'Erro ao ao atualizar'})
  
# Visualiza informçôes do perfil de outro usuário
@bp.route('/user/<username>', methods=['GET'])
def user(username):
  if not current_user.is_authenticated:
    return redirect(url_for('auth.signin', next = url_for('main.user', username = username)))
  user = User.query.filter_by(username = username).first_or_404()
  user = db.session.scalar(sa.select(User).filter_by(username = username))
  if user is None:
    flash('Usuário não existe.')
    return redirect(url_for('main.index'))
  
  return render_template('main/user.html', user = user, title = 'Usuário')

# Carrega dados de um usuário
@bp.route('/get-user-other', methods=['GET'])
def get_user_other():
  user = db.session.scalar(sa.select(User).where(User.username == request.args.get('username')))
  return jsonify({'user_other': render_template('main/user_other.html', user=user)})

# Atualiza os dados de um usuário
@bp.route('/edit-user-other', methods=['POST'])
def edit_user_other():
  if request.method == 'POST':
    user = db.session.scalar(sa.select(User).where(User.username == request.form['username']))
    if user is not None:
      user.username = request.form['username']
      user.name = request.form['name']
      user.email = request.form['email']
      user.website = request.form['website']
      user.profission = request.form['profission']
      user.address = request.form['address']
      user.github = request.form['github']
      db.session.commit()
      return jsonify({'msg': 'Usuário atualizado com sucesso!'})
    else:
      return jsonify({'msg': 'Erro ao ao atualizar'})

# Envia mensagem para um usuário
@bp.route('/send-message', methods = ['GET', 'POST'])
def send_message():
  if request.method == 'POST':
    user = db.first_or_404(sa.select(User).where(User.username == request.form['recipient']))
    message = Message(
      message_author=current_user, 
      recipient_author=user, 
      body=request.form['message'])
    db.session.add(message)
    user.add_notification('unread_message_count', user.unread_message_count())
    db.session.commit()
    return jsonify({'msg': f'Sua mensagem tem sido enviada para {request.form["recipient"]}!'})
  
# Ver todas as mensagens
@bp.route('/messages')
def messages():
  current_user.last_message_read_time = datetime.now(timezone.utc)
  current_user.add_notification('unread_message_count', 0)
  db.session.commit()
  page = request.args.get('page', 1, type = int)
  query = current_user.messages_received.select().order_by(Message.timestamp.desc())
  messages = db.paginate(query, page = page, per_page = current_app.config['PER_PAGE_MESSAGES'], error_out = False)
  prev_url = url_for('main.messages', page = messages.prev_num) if messages.has_prev else None
  next_url = url_for('main.messages', page = messages.next_num) if messages.has_next else None
  
  return render_template('main/messages.html', messages = messages.items, prev_url = prev_url, next_url = next_url, title = "Mensagens")

# Ver todas as notificaçôes
@bp.route('/notifications')
def notifications():
  since = request.args.get('since', 0.0, type = float)
  query = current_user.notifications.select().where(Notification.timestamp > since).order_by(Notification.timestamp.asc())
  notifications = db.session.scalars(query)
  return [{
      'name': n.name, 
      'data': n.get_data(), 
      'timestamp': n.timestamp} for n in notifications]

# Renderiza comunidade
@bp.route('/community')
def community():
  return render_template('main/community.html')

# Pega todos os comentários 
@bp.route('/get-comments', methods=['GET'])
def getComments():
  page = request.args.get('page', 1, type = int)
  query = sa.select(Comment).order_by(Comment.created.desc())
  comments = db.paginate(query, page = page, per_page = current_app.config['PER_PAGE_COMMENTS'], error_out = False)
  next_url = url_for('main.getComments', page = comments.next_num) if comments.has_next else None
  prev_url = url_for('main.getComments', page = comments.prev_num) if comments.has_prev else None
  return jsonify({'comments': render_template('main/get_comments.html', comments = comments.items, next_url = next_url, prev_url = prev_url)})

# Adiciona um comentário  
@bp.route('/add-comment', methods = ['POST'])
def addComment():
  if request.method == 'POST':
    comment = Comment(content = request.form['comment'], comment_author = current_user._get_current_object())
    db.session.add(comment)
    db.session.commit()
    return jsonify({'msg': 'Comentário publicado com sucesso!'})

# Pega informaçôes do comentário
@bp.route('/get-data-comment')
def getDataComment():
  comment = Comment.query.get(request.args.get('comment_id'))
  return jsonify({'form': render_template('main/comment.html', comment = comment)})

# Edita um comentário
@bp.route('/edit-comment', methods = ['POST'])
def editComment():
  comment = Comment.query.get(request.form['comment_id'])
  if comment is not None:
    comment.content = request.form['comment']
    db.session.commit()
    return jsonify({'msg': 'Comentário atualizado com sucesso!'})
  else:
    return jsonify({'msg': 'Comentário não existe!'})
 
# Deleta um comentário   
@bp.route('/delete-comment')
def deleteComment():
  comment = Comment.query.get(request.args.get('comment_id'))
  if comment is not None:
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'msg': 'Comentário deletado com sucesso!'})
  else:
    return jsonify({'msg': 'Comentário não existe!'})