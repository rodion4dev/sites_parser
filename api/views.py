"""Набор endpoint'ов интерфейса с вспомогательными инструментами."""
import json
from http import HTTPStatus
from logging import getLogger
from urllib.parse import urlparse
from uuid import UUID

from celery.result import AsyncResult
from flask import Blueprint, abort, jsonify, request
from redis import Redis, ConnectionError as RedisConnectionError

from api import celery
from api.settings import config

blueprint = Blueprint('views', __name__, url_prefix='/')


@blueprint.errorhandler(HTTPStatus.BAD_REQUEST.value)
def bad_request(error):
    """Обработка ошибки 400: Неверный запрос."""
    return jsonify(error=error.description), HTTPStatus.BAD_REQUEST.value


@blueprint.errorhandler(HTTPStatus.NOT_FOUND.value)
def resource_not_found(error):
    """Обработка ошибки 404: Ресурс не найден."""
    return jsonify(error=error.description), HTTPStatus.NOT_FOUND.value


@blueprint.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR.value)
def internal_server_error(error):
    """Обработка ошибки 500: Внутренняя ошибка сервера."""
    return (jsonify(error=error.description), HTTPStatus.INTERNAL_SERVER_ERROR.value)


@blueprint.route('/task/<uuid:identifier>', methods=['GET'])
def get_task(identifier: UUID):
    """Получения состояния задачи."""
    try:
        redis = Redis(
            host=config.CELERY_RESULTS_BACKEND_HOST,
            port=config.CELERY_RESULTS_BACKEND_PORT,
            db=config.CELERY_RESULTS_BACKEND_VIRTUAL_HOST,
            decode_responses=True,
        )
        task = redis.get(f'celery-task-meta-{identifier}')
    except RedisConnectionError as error:
        getLogger(__name__).critical(f'Ошибка соединения с Redis: {error}')
        abort(500, description='Ошибка на стороне сервера, попробуйте позже.')
        return

    if not task:
        abort(HTTPStatus.NOT_FOUND.value, description='Задача не найдена.')

    return jsonify(json.loads(task))


def url_is_valid(url: str) -> bool:
    """
    Проверка корректности передаваемого ресурса.

    TODO: Не совсем верный подход; можно улучшить.
    """
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc, parsed_url.path])


@blueprint.route('/task', methods=['POST'])
def create_task():
    """Создание задачи."""
    site_url = request.get_json().get('site_url', '')
    if not url_is_valid(site_url):
        abort(HTTPStatus.BAD_REQUEST.value, description='Указанный URL некорректный.')
        return

    result: AsyncResult = celery.application.send_task(
        'parse.tasks.parse_site', args=[site_url]
    )
    return jsonify(identifier=result.id), 201
