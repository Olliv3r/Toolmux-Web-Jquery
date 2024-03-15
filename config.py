from os import getenv, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))

class Config:
  load_dotenv()
  SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'toolmux.db')
  #SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{getenv('MYSQL_USER')}:{getenv('MYSQL_PASSWORD')}@{getenv('MYSQL_HOST')}/{getenv('MYSQL_DB')}"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECRET_KEY = getenv("SECRET_KEY")
  PER_PAGE_TOOLS = 10
  PER_PAGE_USERS = 10
  PER_PAGE_COMMENTS = 10
  PER_PAGE_MESSAGES = 10
  confirm_deleted_rows = False
  TOOLMUX_ADMIN = 'toolmux1@gmail.com'
  MAIL_SERVER = getenv('MAIL_SERVER')
  MAIL_PORT = int(getenv('MAIL_PORT'))
  MAIL_USE_TLS = getenv('MAIL_USE_TLS')
  MAIL_USERNAME = getenv('MAIL_USERNAME')
  MAIL_PASSWORD = getenv('MAIL_PASSWORD')
  ADMINS = ['toolmux1@gmail.com']
  MAX_CONTENT_LENGTH = 1024 * 1024
  UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif']
  UPLOAD_PATH = 'app/static/images/avatars'