from apiflask import APIFlask

from Auth import user, admin, commands
from Auth.extensions import db, jwt, redis_client


def create_app(config_object="Auth.config.config"):
    app = APIFlask(__name__, title="Auth API", version="1.0")
    app.config.from_object(config_object)

    register_extensions(app)

    app.app_context().push()
    db.create_all()

    register_blueprints(app)
    register_commands(app)
    return app


def register_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    redis_client.init_app(app)


def register_blueprints(app):
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(admin.views.blueprint)


def register_commands(app):
    app.cli.add_command(commands.create_superuser)
