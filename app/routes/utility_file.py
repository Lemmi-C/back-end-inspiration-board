from flask import abort, make_response

def validate_object(cls,object_id):
    try:
        object_id = int(object_id)
    except:
        abort(make_response({"message":f"{cls.__name__.lower()} {object_id} invalid"}, 400))

    obj = cls.query.get(object_id)

    if not obj:
        abort(make_response({"message":f"{cls.__name__.lower()} {object_id} not found"}, 404))

    return obj

#works and validates empty string but doesn't return both if both are empty(still wont post though), can adjust later
def validate_field_not_empty(field_name, value):
    if not value:
        error_message = f"{field_name.capitalize()} is empty"
        abort(make_response({"message": error_message}, 400))



