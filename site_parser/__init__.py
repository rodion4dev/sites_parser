from flask import Flask

from site_parser.settings import config


def create_application() -> Flask:
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_object(config)

    from site_parser import api
    application.register_blueprint(api.blueprint)

    return application
