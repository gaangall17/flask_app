from flask import Flask
from flask_bootstrap import Bootstrap
from .config import Config
from .auth import auth

def create_app():
    application = Flask(__name__)
    bootstrap = Bootstrap(application) #Init bootstrap

    application.config.from_object(Config)
    application.register_blueprint(auth)

    return application