from flask import Flask
from flask_mail import Mail

app = Flask(__name__)

# Configurações do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'rpa.malafaia@gmail.com'
# cleoalves.p.e@gmail.com
app.config['MAIL_PASSWORD'] = 'kxsw zyza mmjy atsm'
app.config['MAIL_DEFAULT_SENDER'] = 'rpa.malafaia@gmail.com'
# contato@alemdopedal.com

mail = Mail(app)

from alemdopedal import rotas