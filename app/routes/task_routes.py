from flask import Blueprint, request
from app.routes.routes_helper_utilities import create_model_inst_from_dict_with_response, retrieve_model_inst_by_id
from app.models.task import Task

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

# CREATE ONE TASK
@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model_inst_from_dict_with_response(Task, request_body)

# READ ALL TASKS
@bp.get("")
def get_all_tasks():
    query = db.select(Task).order_by(id)
    tasks = db.session.scalars(query)
    
    response = []
    for task in tasks:
        response.append(task.to_dict())
    
    return response

# READ ONE TASK BY ID
@bp.get("/<task_id>")
def get_task_by_id(task_id):
    task = retrieve_model_inst_by_id(Task, task_id)

    return task.to_dict()

# UPDATE ONE TASK

# PATCH ONE TASK

# DELETE ONE TASK

# DELETE ALL TASKS