from logging import getLogger
from uuid import UUID

from flask import Blueprint, abort, jsonify
from redis import Redis, ConnectionError as RedisConnectionError

from site_parser import config

blueprint = Blueprint('api', __name__, url_prefix='/api/')
redis = Redis(host=config.REDIS_DATABASE_HOSTNAME,
              port=config.REDIS_DATABASE_PORT, db=config.REDIS_DATABASE_NUMBER,
              decode_responses=True)


@blueprint.errorhandler(404)
def resource_not_found(error):
    return jsonify(error=error.description), 404


@blueprint.errorhandler(500)
def internal_server_error(error):
    return jsonify(error=error.description), 500


@blueprint.route('/task/<uuid:identifier>/status', methods=['GET'])
def get_task(identifier: UUID):
    """Получения состояния задачи."""
    try:
        status_summary = redis.get(str(identifier))
        if status_summary:
            return jsonify(summary=status_summary)
        else:
            abort(404, description='Объекта с таким идентификатором не '
                                   'найдено.')
    except RedisConnectionError as error:
        getLogger(__name__).critical(f'Что-то пошло не так в момент '
                                     f'соединения с Redis. Ошибка: {error}')
        abort(500, description='На сервере проблема, повторите попытку позже.')


@blueprint.route('/task', methods=['POST'])
def create_task():
    """Создание задачи."""
    return {}
