from http import HTTPStatus
from urllib.parse import urlparse
from uuid import UUID

from celery.result import AsyncResult
from flask import Blueprint, abort, jsonify, request

from api import celery

blueprint = Blueprint('views', __name__, url_prefix='/')


@blueprint.errorhandler(HTTPStatus.BAD_REQUEST.value)
def resource_not_found(error):
    return jsonify(error=error.description), HTTPStatus.BAD_REQUEST.value


@blueprint.errorhandler(HTTPStatus.NOT_FOUND.value)
def resource_not_found(error):
    return jsonify(error=error.description), HTTPStatus.NOT_FOUND.value


@blueprint.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR.value)
def internal_server_error(error):
    return (jsonify(error=error.description),
            HTTPStatus.INTERNAL_SERVER_ERROR.value)


@blueprint.route('/task/<uuid:identifier>/status', methods=['GET'])
def get_task(identifier: UUID):
    """Получения состояния задачи."""
    return jsonify()


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
        abort(HTTPStatus.BAD_REQUEST.value,
              description='Указанный URL некорректный.')
        return

    result: AsyncResult = celery.application.send_task('tasks.parse_site',
                                                       args=[site_url])
    return jsonify(identifier=result.id)
