from flask import Blueprint, request, Response, make_response, abort
from sqlalchemy import desc
from datetime import datetime, timezone
import requests
from app.routes.routes_helper_utilities import create_model_inst_from_dict_with_response, retrieve_model_inst_by_id, nested_dict
from app.models.task import Task
from app.models.goal import Goal
from app.db import db

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

# POST ONE GOAL, RETURN {"GOAL": {GOAL DICTIONARY}}
@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model_inst_from_dict_with_response(Goal, request_body)

# ADD EXISTING TASK IDS TO EXISTING GOAL, RETURN {"ID":..., "TASK_IDS": [...]}
@bp.post("/<goal_id>/tasks")
def add_task_ids_to_goal(goal_id):
    goal = retrieve_model_inst_by_id(Goal, goal_id)
    request_body = request.get_json()

    # remove existing task from that goal
    query = db.select(Task).where(Task.goal_id==1)
    old_tasks = db.session.scalars(query)
    for task in old_tasks:
        task.goal_id = None

    # add tasks to the goal
    for task_id in request_body["task_ids"]:
        task = retrieve_model_inst_by_id(Task, task_id)
        task.goal_id = goal_id    

    db.session.commit()
    return {"id": int(goal_id),
            "task_ids": [task.id for task in goal.tasks]}

# GET TASKS FOR ONE GOAL, RETURN GOAL DICTIONARY WITH TASKS LIST
@bp.get("/<goal_id>/tasks")
def get_tasks_of_one_goal(goal_id):
    goal = retrieve_model_inst_by_id(Goal, goal_id)
    return goal.to_dict(include_empty_tasks=True)

# GET ALL GOALS
@bp.get("")
def get_saved_goals():
    goals = db.session.scalars(db.select(Goal).order_by(Goal.id))
    return [goal.to_dict() for goal in goals]

# GET GOAL BY ID
@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = retrieve_model_inst_by_id(Goal, goal_id)
    return nested_dict(Goal, goal)

# UPDATE GOAL TITLE
@bp.put("/<goal_id>")
def update_one_goal(goal_id):
    goal = retrieve_model_inst_by_id(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")

# DELETE ONE GOAL
@bp.delete("/<goal_id>")
def delete_one_goal(goal_id):
    goal = retrieve_model_inst_by_id(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


