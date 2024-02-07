from app import db
from datetime import datetime

categories = ["Information Collection", "Vulnerability Analysis", "Wireless Attacks", "Web Applications", "Sniffing and Faking", "Maintaining Access", "Reporting Tools", "Exploitation Tools", "Forensic Tools", "Stress Test", "Password Attacks", "Reverse Engineering", "Hardware Hacking", "Extra"]
installation_types = ["apt", "git"]
situations = ['Active', 'Inactive', 'Waiting']

class Tool(db.Model):
  __tablename__ = 'tools'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(30), nullable = False)
  alias = db.Column(db.String(30), nullable = False)
  executable = db.Column(db.String(30))
  name_repo = db.Column(db.String(30))
  link = db.Column(db.String(60))
  dependencies = db.Column(db.String(500))
  category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
  installation_type_id = db.Column(db.Integer, db.ForeignKey('installation_types.id'))
  author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
  situation_id = db.Column(db.Integer, db.ForeignKey('situations.id'))
  installation_tip = db.Column(db.String(500))
  description = db.Column(db.String(500))
  created = db.Column(db.DateTime, default = datetime.utcnow)
  modified = db.Column(db.DateTime, default = datetime.utcnow)
  
class Category(db.Model):
  __tablename__ = 'categories'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(30), nullable = False)
  tools = db.relationship('Tool', backref = 'category', lazy = 'dynamic')
  created = db.Column(db.DateTime, default = datetime.utcnow)
  modified = db.Column(db.DateTime, default = datetime.utcnow)
  
  def __repr__(self):
    return f'<{self.name}>'
  
  # Insere as categorias na base se caso não existam
  @staticmethod
  def insert_categories():
    for c in categories:
      category = Category.query.filter_by(name = c).first()
      if category is None:
        category = Category(name = c)
        db.session.add(category)
    db.session.commit()

  # Adiciona uma categoria
  @staticmethod
  def add_category(name):
    if Category.query.filter_by(name = name).first() is not None:
      return False
    else:
       category = Category(name = name)
       db.session.add(category)
       db.session.commit()
       return True

  # Remove uma categoria
  @staticmethod
  def remove_category(name):
    category = Category.query.filter_by(name = name).first()
    if category is not None:
      db.session.delete(category)
      db.session.commit()
      return True
    else:
      return False

  # Ver todas as categorias
  @staticmethod
  def view_categories():
    for category in Category.query.all():
      print(category)
  
class InstallationType(db.Model):
  __tablename__ = 'installation_types'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(30), nullable = False)
  tools = db.relationship('Tool', backref = 'installation_type', lazy = 'dynamic')
  created = db.Column(db.DateTime, default = datetime.utcnow)
  modified = db.Column(db.DateTime, default = datetime.utcnow)
  
  def __repr__(self):
    return f'<{self.name}>'
  
  # Insere os tipos de instalação na base se caso não existam
  @staticmethod
  def insert_installation_types():
    for it in installation_types:
      installation_type = InstallationType.query.filter_by(name = it).first()
      if installation_type is None:
        installation_type = InstallationType(name = it)
        db.session.add(installation_type)
    db.session.commit()

  # Adiciona um tipo de instalaçäo
  @staticmethod
  def add_installation_type(name):
    if InstallationType.query.filter_by(name = name).first() is not None:
      return False
    else:
       installation_type = InstallationType(name = name)
       db.session.add(installation_type)
       db.session.commit()
       return True

  # Remove um tipo de instalação
  @staticmethod
  def remove_installation_type(name):
    installation_type = InstallationType.query.filter_by(name = name).first()
    if installation_type is not None:
      db.session.delete(installation_type)
      db.session.commit()
      return True
    else:
      return False

  # Ver todos os tipos de instalação
  @staticmethod
  def view_installation_types():
    for installation_type in InstallationType.query.all():
      print(installation_type)
  
class Author(db.Model):
  __tablename__ = 'authors'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(30), nullable = False)
  github = db.Column(db.String(100), nullable = True)
  tools = db.relationship('Tool', backref = 'author', lazy = 'dynamic')
  created = db.Column(db.DateTime, default = datetime.utcnow)
  modified = db.Column(db.DateTime, default = datetime.utcnow)
  
  def __repr__(self):
    return f'<{self.name}>'
    
  # Ver todos os tipos autores
  @staticmethod
  def view_authors():
    for author in Author.query.all():
      print(author.name)

class Situation(db.Model):
  __tablename__ = 'situations'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(30), nullable = False)
  tools = db.relationship('Tool', backref = 'situation', lazy = 'dynamic')
  created = db.Column(db.DateTime, default = datetime.utcnow)
  modified = db.Column(db.DateTime, default = datetime.utcnow)

  def __repr__(self):
    return f'<{self.name}>'

  @staticmethod
  def insert_situations():
    for sit in situations:
      if Situation.query.filter_by(name = sit).first() is None:
        situation = Situation(name = sit)
        db.session.add(situation)
    db.session.commit()

  @staticmethod
  def view_situations():
    for situation in Situation.query.all():
      print(situation.name)

  @staticmethod
  def add_situation(name):
    if Situation.query.filter_by(name = name).first() is not None:
      return False
    else:
      situation = Situation(name = name)
      db.session.add(situation)
      db.session.commit()
      return True

  @staticmethod
  def remove_situation(name):
    situation = Situation.query.filter_by(name = name).first()
    if situation is not None:
      db.session.delete(situation)
      db.session.commit()
      return True
    else:
      return False
