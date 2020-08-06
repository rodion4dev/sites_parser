from uuid import UUID

from flask import Blueprint

blueprint = Blueprint('api', __name__, url_prefix='/api/')


@blueprint.route('/task/<uuid:identifier>', methods=['GET'])
def get_task(identifier: UUID):
    """Получения состояния задачи."""
    return {'identifier': identifier}


@blueprint.route('/task', methods=['POST'])
def create_task():
    """Создание задачи."""
    return {}
