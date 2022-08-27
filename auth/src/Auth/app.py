from flask import Flask

from Auth import user
from Auth.db.common import engine
from Auth.db.models import Base
from Auth.extensions import db, jwt, redis_client


def create_app(config_object="Auth.config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_extensions(app)

    Base.metadata.create_all(engine)

    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    redis_client.init_app(app)


def register_blueprints(app):
    app.register_blueprint(user.views.blueprint)
