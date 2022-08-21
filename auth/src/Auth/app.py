from flask import Flask

from Auth.db.common import engine
from Auth.db.models import Base
from Auth.extensions import db


def create_app(config_object="Auth.config"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    Base.metadata.create_all(engine)
    return app


def register_extensions(app):
    db.init_app(app)
