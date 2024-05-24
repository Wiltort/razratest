from app.api import bp
from flask import jsonify
from app.models import Task, User

@bp.route('/tasks', methods=['POST'])
def post_task():
    pass

@bp.route('/tasks', methods=['GET'])
def get_tasks(id):
    return jsonify(Task.query.get_or_404(id).to_dict())