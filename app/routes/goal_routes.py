from flask import Blueprint, request, Response, make_response, abort
from sqlalchemy import desc
from datetime import datetime, timezone
import requests
from app.routes.routes_helper_utilities import create_model_inst_from_dict_with_response, retrieve_model_inst_by_id, nested_dict
from app.models.task import Task
from app.models.goal import Goal
from app.db import db

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model_inst_from_dict_with_response(Goal, request_body)

@bp.get("")
def get_saved_goals():
    goals = db.session.scalars(db.select(Goal).order_by(Goal.id))
    return [goal.to_dict() for goal in goals]

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = retrieve_model_inst_by_id(Goal, goal_id)
    return nested_dict(Goal, goal)



