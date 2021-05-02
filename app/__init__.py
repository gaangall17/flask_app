from flask import Flask
from flask_bootstrap import Bootstrap
from .config import Config
from .auth import auth

def create_app():
    application = app = Flask(__name__)
    bootstrap = Bootstrap(app) #Init bootstrap

    app.config.from_object(Config)
    app.register_blueprint(auth)

    return app