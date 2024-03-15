from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_mail import Mail
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

bootstrap = Bootstrap4()
db = SQLAlchemy()
moment = Moment()
login = LoginManager()
login.login_view = 'auth.signin'
mail = Mail()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  bootstrap.init_app(app)
  db.init_app(app)
  moment.init_app(app)
  login.init_app(app)
  mail.init_app(app)
  
  # Blueprint registrados
  from .main import bp as main_bp
  app.register_blueprint(main_bp)
  from .dashboard import bp as dashboard_bp
  app.register_blueprint(dashboard_bp)
  from .auth import bp as auth_bp
  app.register_blueprint(auth_bp, url_prefix = '/auth')
  from .errors import bp as errors_bp
  app.register_blueprint(errors_bp)
  from .test import bp as test_bp
  app.register_blueprint(test_bp)
  
  if not app.debug:
    if app.config['MAIL_SERVER']:
      auth = None
      if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        
      secure = None
      if app.config['MAIL_USE_TLS']:
        secure = ()
      
      mail_handler = SMTPHandler(
        mailhost=(
          app.config['MAIL_SERVER'], 
          app.config['MAIL_PORT']
        ),
        fromaddr='no-reply@' + app.config['MAIL_SERVER'],
        toaddrs=app.config['ADMINS'], 
        subject='Toolmux failure',
        credentials=auth, secure=secure
      )
      mail_handler.setLevel(logging.ERROR)
      app.logger.addHandler(mail_handler)
  
    if not os.path.exists('logs'):
      os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/toolmux.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(
      logging.Formatter(
      '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
      )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Toolmux startup')
  
  return app
from app import models