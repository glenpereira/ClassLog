from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import jinja2

UPLOAD_FOLDER = 'mainface/static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'MP4', 'MOV', 'JPG', 'PNG', "JPEG"])
PICTURE_EXTENSIONS = ['.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']
ALLOWED_EXTENSIONS_VIDEO = set(['mp4', 'mov', 'MP4', 'MOV'])
UPLOAD_BUCKET = "classlogpublic"
FACE_BUCKET = "classlog"

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)
app.secret_key = "goodnight"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object("mainface.config")

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from mainface import routes