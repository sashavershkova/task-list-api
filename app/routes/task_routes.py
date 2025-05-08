from flask import Blueprint, request, Response, make_response, abort
from sqlalchemy import desc
from datetime import datetime, timezone
import requests
from app.routes.routes_helper_utilities import create_model_inst_from_dict_with_response, retrieve_model_inst_by_id
from app.models.task import Task
from app.db import db
import os

slack_token = os.environ.get("SLACKBOT_TOKEN")

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


# CREATE ONE TASK
@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model_inst_from_dict_with_response(Task, request_body)


# READ ALL TASKS
@bp.get("")
def get_all_tasks():
    query = db.select(Task)

    sort_param = request.args.get("sort")
    if sort_param=="desc":
        query = query.order_by(desc(Task.title))
    else:
        query = query.order_by(Task.title)

    query = query.order_by(Task.id)
    tasks = db.session.scalars(query)
    
    response = []
    for task in tasks:
        response.append(task.to_dict())
    
    return response


# READ ONE TASK BY ID
@bp.get("/<task_id>")
def get_task_by_id(task_id):
    task = retrieve_model_inst_by_id(Task, task_id)

    return {"task": task.to_dict()}


# UPDATE ONE TASK
@bp.put("/<task_id>")
def update_by_id(task_id):
    task = retrieve_model_inst_by_id(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")


# PATCH ONE TASK
@bp.patch("/<task_id>")
def patch_by_id(task_id):
    task = retrieve_model_inst_by_id(Task, task_id)
    request_body = request.get_json()

    if "title" in request_body:
        task.title = request_body["title"]
    if "description" in request_body:
        task.description = request_body["description"]      
    if "completed_at" in request_body:
        task.completed_at = request_body["completed_at"]
    
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# PATCH ONE TASK MARK IT AS COMPLETE
@bp.patch("/<task_id>/mark_complete")
def patch_by_id_mark_complete(task_id):
    task = retrieve_model_inst_by_id(Task, task_id)

    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()
    
    # send notification to Slack
    headers = {"Authorization": f"Bearer {slack_token}"}
    data = {
        "channel": "C08NTC26TM1",
        "text": f"Someone just completed the task -- {task.title}: {task.description}"
    }

    requests.post("https://slack.com/api/chat.postMessage", headers=headers, data=data)

    return Response(status=204, mimetype="application/json")


# PATCH ONE TASK MARK IT AS INCOMPLETE
@bp.patch("/<task_id>/mark_incomplete")
def patch_by_id_mark_incomplete(task_id):
    task = retrieve_model_inst_by_id(Task, task_id)

    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# DELETE ONE TASK
@bp.delete("/<task_id>")
def delete_by_id(task_id):
    task = retrieve_model_inst_by_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


# DELETE ALL TASKS
@bp.delete("")
def delete_all_tasks():
    db.session.query(Task).delete()
    db.session.commit()

    return Response(status=204, mimetype="application/json")
