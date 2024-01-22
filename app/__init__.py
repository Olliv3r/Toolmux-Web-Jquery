from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment

bootstrap = Bootstrap5()
db = SQLAlchemy()
moment = Moment()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  bootstrap.init_app(app)
  db.init_app(app)
  moment.init_app(app)
  
  from .tool import bp as tool_bp
  app.register_blueprint(tool_bp)
  
  from .main import bp as main_bp
  app.register_blueprint(main_bp)
  
  from app import models
  return app
  