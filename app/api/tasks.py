from app.api import bp
from flask import jsonify, g, request, abort
from app.models import Task, User
from app.api.auth import token_auth
from app import db
from app.api.errors import bad_request
import sqlalchemy as sa


@bp.route('/tasks', methods=['POST'])
@token_auth.login_required
def create_task():
    '''Создаем новую задачу'''
    data = request.get_json()
    if 'title' not in data:
        return bad_request('must include title')
    owner = g.current_user
    task = Task()
    task.from_dict(data, owner_user=owner)
    db.session.add(task)
    db.session.commit()
    response = jsonify(task.to_dict())
    response.status_code = 201
    return response


@bp.route('/tasks', methods=['GET'])
@token_auth.login_required
def get_tasks():
    '''список задач текущего юзера'''
    tasks = Task.query.filter_by(owner=g.current_user).order_by(Task.created_at)
    data = [item.to_dict() for item in tasks]
    return jsonify(data)


@bp.route('/tasks/<int:id>', methods=['GET'])
@token_auth.login_required
def get_task(id):
    '''выдача задачи'''
    task = db.get_or_404(Task, id)
    if task.owner != g.current_user:
        abort(403)
    return jsonify(task.to_dict())


@bp.route('/tasks/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_task(id):
    '''редактирование задачи'''
    task = db.get_or_404(Task, id)
    owner = g.current_user
    if task.owner != owner:
        abort(403)
    data = request.get_json()
    task.from_dict(data=data, owner_user=owner)
    db.session.commit()
    return jsonify(task.to_dict())


@bp.route('/tasks/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_task(id):
    '''удаление задачи'''
    task = db.get_or_404(Task, id)
    owner = g.current_user
    if task.owner != owner:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    response = jsonify({"result": f"the task {task} deleted"})
    response.status_code = 200
    return response