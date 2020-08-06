from flask import Blueprint, jsonify

blueprint = Blueprint('views', __name__, url_prefix='/')


@blueprint.errorhandler(404)
def resource_not_found(error):
    return jsonify(error=error.description), 404


@blueprint.errorhandler(500)
def internal_server_error(error):
    return jsonify(error=error.description), 500


@blueprint.route('/task/<int:identifier>/status', methods=['GET'])
def get_task(identifier: int):
    """Получения состояния задачи."""
    return jsonify()


@blueprint.route('/task', methods=['POST'])
def create_task():
    """Создание задачи."""
    return jsonify()
