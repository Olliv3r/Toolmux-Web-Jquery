from app import db
from datetime import datetime

class Tool(db.Model):
  __tablename__ = 'tools'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(30), nullable = False)
  author = db.Column(db.String(30), nullable = False)
  alias = db.Column(db.String(30), nullable = False)
  custom_alias = db.Column(db.String(30))
  name_repo = db.Column(db.String(30))
  link = db.Column(db.String(60))
  dependencies = db.Column(db.String(500))
  category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
  type_install_id = db.Column(db.Integer, db.ForeignKey('typesinstall.id'))
  installation_tip = db.Column(db.String(500))
  created = db.Column(db.DateTime, default = datetime.utcnow)
  modified = db.Column(db.DateTime, default = datetime.utcnow)
  
class Category(db.Model):
  __tablename__ = 'categories'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(30), nullable = False)
  tools = db.relationship('Tool', backref = 'category', lazy = 'dynamic')
  created = db.Column(db.DateTime, default = datetime.utcnow)
  modified = db.Column(db.DateTime, default = datetime.utcnow)
  
class TypeInstall(db.Model):
  __tablename__ = 'typesinstall'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(30), nullable = False)
  tools = db.relationship('Tool', backref = 'type_install', lazy = 'dynamic')
  created = db.Column(db.DateTime, default = datetime.utcnow)
  modified = db.Column(db.DateTime, default = datetime.utcnow)
  
