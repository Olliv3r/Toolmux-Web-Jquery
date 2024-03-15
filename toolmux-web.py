from app import create_app
from app import db
from flask_migrate import Migrate
import sqlalchemy as sa
from app.models import insert_all, insert_users

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_processor():
  return {'sa': sa, 'insert_all': insert_all, 'insert_users': insert_users}