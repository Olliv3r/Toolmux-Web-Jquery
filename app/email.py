from threading import Thread
from flask_mail import Message
from app import mail
from flask import current_app, render_template

def send_async_email(app, msg):
  with app.app_context():
    mail.send(msg)

# Envia e-mail
def send_email(subject, sender, recipients, text_body, html_body):
  msg = Message(subject, sender=sender, recipients=recipients)
  msg.body = text_body
  msg.html = html_body
  Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
  
# Envia redefinição de senha
def send_password_reset_email(user):
  token = user.get_reset_password_token()
  send_email('[Toolmux] Redefinir sua senha', sender=current_app.config['ADMINS'][0], recipients=[user.email], text_body = render_template('email/reset_password.txt', user = user, token = token), html_body = render_template('email/reset_password.html', user = user, token = token))
  
# Envia confirmação de conta
def send_confirmation_email(user):
  token = user.get_confirmation_account_token()
  send_email('[Toolmux] Confirme sua conta', sender=current_app.config['ADMINS'][0], recipients = [user.email], text_body = render_template('email/confirm_account.txt', token = token, user = user), html_body = render_template('email/confirm_account.html', user = user, token = token))