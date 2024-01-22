from os import environ, path

basedir = path.abspath(path.dirname(__file__))

class Config:
  SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + path.join(basedir, 'toolmux.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECRET_KEY = "toolmux.?!@8268377#"
  PER_PAGE_TOOLS = 5
  confirm_deleted_rows = False
