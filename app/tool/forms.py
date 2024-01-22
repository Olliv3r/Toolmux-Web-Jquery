from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from app.models import TypeInstall, Category

class ToolAddCreateForm(FlaskForm):
  name = StringField('Nome', validators=[DataRequired()])
  author = StringField('Autor', validators=[DataRequired()])
  alias = StringField('Apelido', validators=[DataRequired()])
  custom_alias = StringField('Apelido personalizado')
  name_repo = StringField('Nome do repositório')
  link = StringField('Link')
  type_install = SelectField("Instalação via" ,coerce = int)
  category = SelectField("Categoria", coerce = int)
  dependencies = StringField('Dependências')
  installation_tip = TextAreaField('Dica de instalação')
  
  def __init__(self, *args, **kwargs):
    super(ToolAddCreateForm, self).__init__(*args, **kwargs)
    self.type_install.choices = [(ti.id, ti.name) for ti in TypeInstall.query.all()]
    self.category.choices = [(cat.id, cat.name) for cat in Category.query.all()]
    
class ToolUpdateCreateForm(FlaskForm):
  name = StringField('Nome', validators=[DataRequired()])
  author = StringField('Autor', validators=[DataRequired()])
  alias = StringField('Apelido', validators=[DataRequired()])
  custom_alias = StringField('Apelido personalizado')
  name_repo = StringField('Nome do repositório')
  link = StringField('Link')
  type_install = SelectField("Instalação via" ,coerce = int)
  category = SelectField("Categoria", coerce = int)
  dependencies = StringField('Dependências')
  installation_tip = TextAreaField('Dica de instalação')
  
  def __init__(self, *args, **kwargs):
    super(ToolUpdateCreateForm, self).__init__(*args, **kwargs)
    self.type_install.choices = [(ti.id, ti.name) for ti in TypeInstall.query.all()]
    self.category.choices = [(cat.id, cat.name) for cat in Category.query.all()]
    
class ToolSearchCreateForm(FlaskForm):
  search_text = StringField('Pesquisar', validators = [DataRequired()])