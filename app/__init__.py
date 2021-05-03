from flask import Flask
from flask_bootstrap import Bootstrap
from .config import Config
from .auth import auth
from .models import UserModel
from flask_login import LoginManager


login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)


def create_app():
    application = Flask(__name__)
    bootstrap = Bootstrap(application) #Init bootstrap

    application.config.from_object(Config)

    login_manager.init_app(application) #Init login manager

    application.register_blueprint(auth)

    return application