from app.api import bp
from flask import jsonify, g, request
from app.models import Task, User
from app.api.auth import token_auth
from app import db
from app.api.errors import bad_request


@bp.route('/tasks', methods=['POST'])
@token_auth.login_required
def create_task():
    '''Создаем новую задачу'''
    data = request.get_json() or {}
    if 'title' not in data:
        return bad_request('must include title')
    #?может ли быть title не уникальным?
    owner = g.current_user
    task = Task()
    task.from_dict(data,owner_user=owner)
    db.session.add(task)
    db.session.commit()
    response = jsonify(task.to_dict())
    response.status_code = 201
    return response


@bp.route('/tasks', methods=['GET'])
@token_auth.login_required
def get_tasks():
    '''список задач текущего юзера'''
    tasks = Task.query.filter_by(owner=g.current_user)
    data = [item.to_dict() for item in tasks]
    return jsonify(data)