import json

import jsonschema
from flask import jsonify, request


def load_json_schema(filename):
    with open(filename, "r") as file:
        schema = json.load(file)
    return schema


def validate_json_schema(schema):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            input_data = request.json

            # Validate the input model against the JSON schema
            try:
                jsonschema.validate(instance=input_data, schema=schema)
            except jsonschema.ValidationError as e:
                return jsonify({"errors": str(e)}), 400

            return fn(*args, **kwargs)

        return wrapper

    return decorator


# json schemas
lock_input_json_schema = load_json_schema("./aca/api/model/input/schemas/lock_input_schema.json")
call_room_json_schema = load_json_schema("./aca/api/model/input/schemas/call_room_schema.json")

# end json schemas
