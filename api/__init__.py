from flask import Flask

from api.settings import config


def create_application() -> Flask:
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_object(config)

    from api import views
    application.register_blueprint(views.blueprint)

    return application
