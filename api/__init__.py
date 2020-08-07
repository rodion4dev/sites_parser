"""
Внешний REST интерфейс проекта для парсинга сайтов.

Текущий модуль инициализации хранит в себе фабрику Flask приложения.
"""
from flask import Flask

from api.settings import config


def create_application() -> Flask:
    """
    Создание Flask приложения.

    Помимо прочего подключается модуль с endpoint'ами и вытаскивается
    конфигурация из Python объекта.

    :return: WSGI приложение для request-response цикла.
    """
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_object(config)

    from api import views

    application.register_blueprint(views.blueprint)

    return application
