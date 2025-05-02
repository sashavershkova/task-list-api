from flask import abort, make_response
from app.db import db

def retrieve_model_instance_by_id(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response_message = {"message": f"{cls.__name__} id <{model_id}> is invalid."}
        abort(make_response(response_message, 400))       
    
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response_message = {"message": f"{cls.__name__} with id <{model_id}> is not found."}
        abort(make_response(response_message, 404))

    return model
