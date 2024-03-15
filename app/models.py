from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from datetime import datetime
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import jwt
import json

# Listas
categories = [
  "Information Collection", 
  "Vulnerability Analysis",
  "Wireless Attacks", 
  "Web Applications", 
  "Sniffing and Faking",
  "Maintaining Access",
  "Reporting Tools",
  "Exploitation Tools", 
  "Forensic Tools", 
  "Stress Test", 
  "Password Attacks",
  "Reverse Engineering", 
  "Hardware Hacking", 
  "Extra"]
installation_types = [
  "apt", 
  "git"]
situations = [
  'Active', 
  'Inactive',
  'Waiting']

# Permissôes de usuários
class Permission:
  FOLLOW = 1
  COMMENT = 2
  WRITE = 4
  MODERATE = 8
  ADMIN = 16

# Tabela de papéis de usuários
class Role(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key = True)
  name: so.Mapped[str] = so.mapped_column(sa.String(36), unique = True)
  users: so.WriteOnlyMapped['User'] = so.relationship(back_populates = 'role', passive_deletes=True)
  default: so.Mapped[Optional[bool]] = so.mapped_column(default = False, index = True)
  permissions: so.Mapped[int] = so.mapped_column()
  created: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)
  modified: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)
  
  def __init__(self, **kwargs):
    super(Role, self).__init__(**kwargs)
    if self.permissions is None:
      self.permissions = 0
      
  def has_permission(self, perm):
    return self.permissions & perm == perm
    
  def add_permission(self, perm):
    if not self.has_permission(perm):
      self.permissions += perm
      
  def remove_permission(self, perm):
    if self.has_permission(perm):
      self.permissions -= perm
      
  def reset_permissions(self):
    self.permissions = 0
    
  @staticmethod
  def insert_roles():
    roles = {
      'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
      'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
      'Administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
    }
    default_role = 'User'
    for r in roles:
      query = sa.select(Role).filter_by(name = r)
      role = db.session.scalar(query)
      
      if role is None:
        role = Role(name = r)
      role.reset_permissions()
      
      for perm in roles[r]:
        role.add_permission(perm)
      role.default = (role.name == default_role)
      db.session.add(role)
    db.session.commit()
    
  @staticmethod
  def view_roles():
    query = sa.select(Role).order_by(Role.id.asc())
    for role in db.session.scalars(query).all():
      print(role.name)
      
# Tabela de situação de usuários
class SituationUser(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key = True)
  name: so.Mapped[str] = so.mapped_column(sa.String(30))
  users: so.WriteOnlyMapped['User'] = so.relationship(back_populates = 'situationuser', passive_deletes=True)
  default: so.Mapped[Optional[bool]] = so.mapped_column(default = False, index = True)
  created: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)
  modified: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)

  def __repr__(self):
    return f'<{self.name}>'

  @staticmethod
  def insert_situations():
    for sit in situations:
      situation = db.session.scalar(sa.select(SituationUser).filter_by(name = sit))
      if situation is None:
        situation = SituationUser(name = sit)
      default_situation = 'Active'
      situation.default = (situation.name == default_situation)
      db.session.add(situation)
    db.session.commit()

  @staticmethod
  def view_situations():
    for situation in db.session.scalars(sa.select(SituationUser)).all():
      print(situation.name)

  @staticmethod
  def add_situation(name):
    if db.session.scalar(sa.select(SituationUser).filter_by(name = name)) is not None:
      return False
    else:
      situation = SituationUser(name = name)
      db.session.add(situation)
      db.session.commit()
      return True

  @staticmethod
  def remove_situation(name):
    situation = db.session.scalar(sa.select(SituationUser).filter_by(name = name))
    if situation is not None:
      db.session.delete(situation)
      db.session.commit()
      return True
    else:
      return False

# Tabela de usuários
class User(UserMixin, db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(30))
  profission: so.Mapped[Optional[str]] = so.mapped_column(sa.String(30))
  address: so.Mapped[Optional[str]] = so.mapped_column(sa.String(30))
  github: so.Mapped[Optional[str]] = so.mapped_column(sa.String(60))
  website: so.Mapped[Optional[str]] = so.mapped_column(sa.String(60))
  username: so.Mapped[str] = so.mapped_column(sa.String(30), index=True, unique=True)
  email: so.Mapped[str] = so.mapped_column(sa.String(30), index=True, unique=True)
  password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
  confirmed: so.Mapped[Optional[bool]] = so.mapped_column(default=False)
  profile_image_url: so.Mapped[Optional[str]] = so.mapped_column(sa.String(360), index=True, unique=True)
  role: so.Mapped[Role] = so.relationship(back_populates='users')
  role_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Role.id))
  situationuser: so.Mapped[SituationUser] = so.relationship(back_populates='users')
  situation_user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(SituationUser.id))
  comments: so.WriteOnlyMapped['Comment'] = so.relationship(back_populates='comment_author', passive_deletes=True)
  messages_sent: so.WriteOnlyMapped['Message'] = so.relationship(foreign_keys="Message.sender_author_id", back_populates="message_author", passive_deletes=True)
  messages_received: so.WriteOnlyMapped['Message'] = so.relationship(foreign_keys="Message.recipient_author_id", back_populates="recipient_author", passive_deletes=True)
  notifications: so.WriteOnlyMapped['Notification'] = so.relationship(back_populates = 'user', passive_deletes=True)
  last_message_read_time: so.Mapped[Optional[datetime]]
  created: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
  modified: so.Mapped[datetime] = so.mapped_column(default=datetime.utcnow)
  
  def __init__(self, **kwargs):
    super(User, self).__init__(**kwargs)
  
    if self.role is None:
      if self.email == current_app.config['TOOLMUX_ADMIN']:
        self.role = db.session.scalar(sa.select(Role).filter_by(name = 'Administrator'))
      # if self.role is None:
      else:
        self.role = db.session.scalar(sa.select(Role).filter_by(default = True))
        
    if self.situationuser is None:
      self.situationuser = db.session.scalar(sa.select(SituationUser).filter_by(default = True))
        
  def can(self, perm):
    return self.role is not None and self.role.has_permission(perm)

  def is_administrator(self):
    return self.can(Permission.ADMIN)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
    
  def get_reset_password_token(self, expires_in=600):
    return jwt.encode(
      {
        'reset_password': self.id, 
        'exp': time() + expires_in
      }, 
      current_app.config['SECRET_KEY'], 
      algorithm='HS256')
    
  @staticmethod
  def verify_reset_password_token(token):
    try:
      id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
    except:
      return
    return db.session.get(User, int(id))
    
  # Gera novo token pra confirmação de conta
  def get_confirmation_account_token(self, expires_in=600):
    return jwt.encode(
      {
        'confirm': self.id,
        'exp': time() + expires_in
      },
      current_app.config['SECRET_KEY'],
      algorithm='HS256')
    
  # Valida token de confirmação da conta
  def verify_confirmation_account_token(self, token):
    try:
      data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
      return False
      
    if data.get('confirm') != self.id:
      return False
    self.confirmed = True
    db.session.add(self)
    return True
    
  def unread_message_count(self):
    last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
    query = sa.select(Message).where(Message.recipient_author == self, Message.timestamp > last_read_time)
    return db.session.scalar(sa.select(sa.func.count()).select_from(query.subquery()))
    
  def add_notification(self, name, data):
    db.session.execute(self.notifications.delete().where(Notification.name == name))
    n = Notification(name=name, payload_json=json.dumps(data), user=self)
    db.session.add(n)
    return n

class AnonymousUser(AnonymousUserMixin):
  def can(self, permissions):
    return False
  
  def is_administrator(self):
    return False
  
# Tabela de comentários de usuários
class Comment(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key = True)
  content: so.Mapped[str] = so.mapped_column(sa.String(300))
  comment_author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
  comment_author: so.Mapped[User] = so.relationship(back_populates = 'comments')
  created: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)
  modified: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)

# Tabela de mensagens de usuários
class Message(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key = True)
  sender_author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
  message_author: so.Mapped[User] = so.relationship(foreign_keys='Message.sender_author_id', back_populates = "messages_sent")
  recipient_author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
  recipient_author: so.Mapped[User] = so.relationship(foreign_keys='Message.recipient_author_id', back_populates = 'messages_received')
  body: so.Mapped[str] = so.mapped_column(sa.String(140))
  timestamp: so.Mapped[datetime] = so.mapped_column(index = True, default = datetime.utcnow)
  
  def __repr__(self):
    return '<Message {}>'.format(self.body)

# Tabela de notificaçôes de usuários
class Notification(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key = True)
  name: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
  user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
  user: so.Mapped[User] = so.relationship(back_populates = 'notifications')
  timestamp: so.Mapped[float] = so.mapped_column(index = True, default = time)
  payload_json: so.Mapped[str] = so.mapped_column(sa.Text)
  
  def get_data(self):
    return json.loads(str(self.payload_json))

# Tabela de categorias de ferramentas
class Category(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key = True)
  name: so.Mapped[str] = so.mapped_column(sa.String(30))
  tools: so.WriteOnlyMapped['Tool'] = so.relationship(back_populates = 'category', passive_deletes=True)
  created: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)
  modified: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)
  
  def __repr__(self):
    return f'<{self.name}>'
  
  # Insere as categorias na base se caso não existam
  @staticmethod
  def insert_categories():
    for c in categories:
      category = db.session.scalar(sa.select(Category).filter_by(name = c))
      if category is None:
        category = Category(name = c)
        db.session.add(category)
    db.session.commit()

  # Adiciona uma categoria
  @staticmethod
  def add_category(name):
    if db.session.scalar(sa.select(Category).filter_by(name = name)) is not None:
      return False
    else:
       category = Category(name = name)
       db.session.add(category)
       db.session.commit()
       return True

  # Remove uma categoria
  @staticmethod
  def remove_category(name):
    category = db.session.scalar(sa.select(Category).filter_by(name = name))
    if category is not None:
      db.session.delete(category)
      db.session.commit()
      return True
    else:
      return False

  # Ver todas as categorias
  @staticmethod
  def view_categories():
    for category in db.session.scalars(sa.select(Category)).all():
      print(category)

# Tabela de tip de instalação de ferramentas
class InstallationType(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key = True)
  name: so.Mapped[str] = so.mapped_column(sa.String(30))
  tools: so.WriteOnlyMapped["Tool"] = so.relationship(back_populates = 'installation_type', passive_deletes=True)
  created: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)
  modified: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)
  
  def __repr__(self):
    return f'<{self.name}>'
  
  # Insere os tipos de instalação na base se caso não existam
  @staticmethod
  def insert_installation_types():
    for it in installation_types:
      installation_type = db.session.scalar(sa.select(InstallationType).filter_by(name = it))
      if installation_type is None:
        installation_type = InstallationType(name = it)
        db.session.add(installation_type)
    db.session.commit()

  # Adiciona um tipo de instalaçäo
  @staticmethod
  def add_installation_type(name):
    if db.session.scalar(sa.select(InstallationType).filter_by(name = name)) is not None:
      return False
    else:
       installation_type = InstallationType(name = name)
       db.session.add(installation_type)
       db.session.commit()
       return True

  # Remove um tipo de instalação
  @staticmethod
  def remove_installation_type(name):
    installation_type = bb.session.scalar(sa.select(InstallationType).filter_by(name = name))
    if installation_type is not None:
      db.session.delete(installation_type)
      db.session.commit()
      return True
    else:
      return False

  # Ver todos os tipos de instalação
  @staticmethod
  def view_installation_types():
    for installation_type in db.session.scalars(sa.select(InstallationType)).all():
      print(installation_type)

# Tabela de autores de ferramentas
class Author(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key = True)
  name: so.Mapped[str] = so.mapped_column(sa.String(30))
  github: so.Mapped[Optional[str]] = so.mapped_column(sa.String(100))
  tools: so.WriteOnlyMapped["Tool"] = so.relationship(back_populates = 'tool_author', passive_deletes=True)
  created: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)
  modified: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)
  
  def __repr__(self):
    return f'<{self.name}>'
    
  # Ver todos os tipos autores
  @staticmethod
  def view_authors():
    for author in db.session.scalars(sa.select(Author)).all():
      print(author.name)
      
# Tabela de situação de ferramentas
class SituationTool(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key = True)
  name: so.Mapped[str] = so.mapped_column(sa.String(30))
  tools: so.WriteOnlyMapped['Tool'] = so.relationship(back_populates = 'situationtool', passive_deletes=True)
  created: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)
  modified: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)

  def __repr__(self):
    return f'<{self.name}>'

  @staticmethod
  def insert_situations():
    for sit in situations:
      if db.session.scalar(sa.select(SituationTool).filter_by(name = sit)) is None:
        situation = SituationTool(name = sit)
        db.session.add(situation)
    db.session.commit()

  @staticmethod
  def view_situations():
    for situation in db.session.scalars(sa.select(SituationTool)).all():
      print(situation.name)

  @staticmethod
  def add_situation(name):
    if db.session.scalar(sa.select(SituationTool).filter_by(name = name)) is not None:
      return False
    else:
      situation = SituationTool(name = name)
      db.session.add(situation)
      db.session.commit()
      return True

  @staticmethod
  def remove_situation(name):
    situation = db.session.scalar(sa.select(SituationTool).filter_by(name = name))
    if situation is not None:
      db.session.delete(situation)
      db.session.commit()
      return True
    else:
      return False
  
# Tabela deferramentas
class Tool(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key = True)
  name: so.Mapped[str] = so.mapped_column(sa.String(30))
  alias: so.Mapped[str] = so.mapped_column(sa.String(30))
  executable: so.Mapped[Optional[str]] = so.mapped_column(sa.String(30))
  name_repo: so.Mapped[Optional[str]] = so.mapped_column(sa.String(30))
  link: so.Mapped[Optional[str]] = so.mapped_column(sa.String(60))
  dependencies: so.Mapped[Optional[str]] = so.mapped_column(sa.String(500))
  category_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Category.id))
  category: so.Mapped[Category] = so.relationship(back_populates = 'tools')
  installation_type_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(InstallationType.id))
  installation_type: so.Mapped[InstallationType] = so.relationship(back_populates = 'tools')
  tool_author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Author.id))
  tool_author: so.Mapped[Author] = so.relationship(back_populates = 'tools')
  situation_tool_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(SituationTool.id))
  situationtool: so.Mapped[SituationTool] = so.relationship(back_populates = 'tools')
  installation_tip: so.Mapped[Optional[str]] = so.mapped_column(sa.String(500))
  description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(500))
  created: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)
  modified: so.Mapped[datetime] = so.mapped_column(default = datetime.utcnow)

def insert_all():
  Role.insert_roles()
  Category.insert_categories()
  InstallationType.insert_installation_types()
  SituationUser.insert_situations()
  SituationTool.insert_situations()

def insert_users():
  u1 = User(
    username='oliveradm', 
    email='toolmux1@gmail.com',
    confirmed=True, 
    role=db.session.scalar(
      sa.select(Role).where(Role.name == 'Administrator')
    )
  )
  u1.set_password('cat')
  db.session.add(u1)
  db.session.commit()

# Carregador de usuários
@login.user_loader
def load_user(id):
  return db.session.get(User, int(id))

login.anonymous_user = AnonymousUser
