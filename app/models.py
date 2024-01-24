from app import db
from datetime import datetime

categories = ["Information Collection", "Vulnerability Analysis", "Wireless Attacks", "Web Applications", "Sniffing and Faking", "Maintaining Access", "Reporting Tools", "Exploitation Tools", "Forensic Tools", "Stress Test", "Password Attacks", "Reverse Engineering", "Hardware Hacking", "Extra"]
installation_types = ["apt", "git"]

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
