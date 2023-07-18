from flask import abort, make_response

#takes class and objects id, checks if int and exists
def validate_object(cls,object_id):
    try:
        object_id = int(object_id)
    except:
        abort(make_response({"error":f"{cls.__name__.lower()} {object_id} invalid"}, 400))
    obj = cls.query.get(object_id)
    
    if not obj:
        abort(make_response({"error":f"{cls.__name__.lower()} {object_id} not found"}, 404))

    return obj

#takes value to be tested and type, checks if empty and correct type
def validate_field(value, expected_type):
    if not value:
        error_message = f"{value} is empty"
        abort(make_response({"error": error_message}, 400))
    
    if not isinstance(value, expected_type):
        error_message = f"{value} is of type {type(value).__name__}, expected {expected_type.__name__}"
        abort(make_response({"error": error_message}, 400))



