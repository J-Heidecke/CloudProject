from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Define flask architecture
app = Flask(__name__)
# Define secret key
app.config['SECRET_KEY'] = 'ec05b867d65fdf756ee9e26be38b9381'
# Define database architecture - SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Define database object
db = SQLAlchemy(app)
# Define bycrypt object
bcrypt = Bcrypt(app)
# Define loginmanager - manages logines. 
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from website import routes