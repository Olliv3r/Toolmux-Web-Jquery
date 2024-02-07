from os import environ, path

basedir = path.abspath(path.dirname(__file__))

class Config:
  SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + path.join(basedir, 'toolmux.db')
  #SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql+pymysql://root:toor@127.0.0.1/toolmux'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECRET_KEY = "toolmux.?!@8268377#"
  PER_PAGE_TOOLS = 5
  confirm_deleted_rows = False

  # MYSQL_HOST = environ.get('MYSQL_HOST') or '127.0.0.1'
  # MYSQL_USER = environ.get('MYSQL_USER') or 'root'
  # MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD') or 'toor'
  # MYSQL_DB = environ.get('MYSQL_DB') or 'tools'
  
