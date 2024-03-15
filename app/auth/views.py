from . import bp
from app import db
from flask import render_template, redirect, url_for, flash, request
from app.models import User
from app.email import send_password_reset_email, send_confirmation_email
from flask_login import login_user, logout_user, login_required, current_user
import sqlalchemy as sa

# Verificar confirmação da conta
@bp.before_app_request
def before_request():
  if current_user.is_authenticated and not current_user.confirmed and request.blueprint != "auth" and request.endpoint != "static":
    return redirect(url_for('auth.unconfirmed'))
  
# Renderiza a página que avisa a confirmação de conta
@bp.route('/unconfirmed')
def unconfirmed():
  if current_user.is_anonymous or current_user.confirmed:
    return redirect(url_for('main.index'))
  return render_template('auth/unconfirmed.html', title = 'Conta não foi confirmada ainda!')
  
# Confirma a conta
@bp.route('/confirm/<token>')
def confirm(token):
  if not current_user.is_authenticated:
    flash('Antes de confirmar sua conta, faça login!', 'alert-warning')
    return redirect(url_for('auth.signin'))
  else:
    if current_user.confirmed:
      return redirect(url_for('main.index'))
    if current_user.verify_confirmation_account_token(token):
      db.session.commit()
      flash('Você confirmou sua conta. Obrigado!')
    else:
      flash('O link de confirmação é inválido ou expirou.', 'alert-danger')
  return redirect(url_for('main.index'))
  
# Re-envia confirmação da conta
@bp.route('/confirm')
def resend_confirm():
  send_confirmation_email(current_user)
  flash('Um novo e-mail de confirmação foi enviado a você por e-mail.', 'alert-warning')
  return redirect(url_for('main.index'))

# Cadastro do usuário
@bp.route('/signup', methods = ['GET', 'POST'])
def signup():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  
  if request.method == "POST":
    user = User(
      username = request.form['username'],
      email = request.form['email'])
    user.set_password(request.form['password'])
    db.session.add(user)
    db.session.commit()
    send_confirmation_email(user)
    flash('Um e-mail de confirmação foi enviado a você por e-mail.!', 'alert-warning')
    return redirect(url_for('auth.signin'))
  return render_template('auth/signup.html', title = 'Se inscrever')

# Acesso do usuário
@bp.route('/signin', methods = ['GET', 'POST'])
def signin():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
    
  if request.method == "POST":
    user = db.session.scalar(sa.select(User).filter_by(username = request.form['username']))
    if user is None or not user.check_password(request.form['password']):
      flash('Usuário ou senha incorreto!', 'alert-danger')
      return redirect(url_for('auth.signin'))
    remember = request.form.get('remember_me') == "on"
    login_user(user, remember = remember)
    next = request.args.get('next') or url_for('main.index')
    return redirect(next)
  return render_template('auth/signin.html', title = 'Entrar')

# Desloga do site
@bp.route('/logout')
def logout():
  if current_user.is_authenticated:
    logout_user()
    return redirect(url_for('main.index'))
  return redirect(url_for('main.index'))

# Envia uma alteração de senha
@bp.route('/reset_password_request', methods = ['GET', 'POST'])
def reset_password_request():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  if request.method == 'POST':
    user = db.session.scalar(sa.select(User).filter_by(email = request.form['email']))
    if user is None:
      flash('O endereço de e-mail é inválido, tente o endereço de e-mail cadastrado no site.')
      return redirect(url_for('auth.reset_password_request'))
    if user:
      send_password_reset_email(user)
    flash('Verifique seu e-mail para obter as instruções para redefinir sua senha.', 'alert-warning')
    return redirect(url_for('auth.signin'))
  return render_template('auth/reset_password_request.html', title = 'Solicitar redefinição de senha')
  
# Altera a senha
@bp.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_password(token):
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  user = User.verify_reset_password_token(token)
  if not user:
    return redirect(url_for('main.index'))
  if request.method == 'POST':
    if request.form['password'] == request.form['password2']:
      user.set_password(request.form['password'])
      db.session.commit()
      flash('Sua senha foi redefinida.', 'alert-success')
      return redirect(url_for('auth.signin'))
    else:
      flash('As senhas não correspondem!')
      return redirect(url_for('auth.reset_password', token=token))
  return render_template('auth/reset_password.html', title = 'Trocar senha')
