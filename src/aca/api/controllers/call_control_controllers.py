import logging
from typing import Optional

from flask import Blueprint, request, jsonify

from aca.api.db.dto.room_dto import put_ongoing_call, find_ongoing_call
from aca.api.db.model.call import Call
from aca.common.schema import validate_json_schema, call_room_json_schema

call_api_bp = Blueprint('call_api', __name__, url_prefix='/api/call')

logger = logging.getLogger(__name__)


@call_api_bp.route("", methods=['POST'], endpoint="call")
@validate_json_schema(call_room_json_schema)
def call():
    logger.debug("Handling POST /api/call")
    room: int = request.get_json()["room"]
    ongoing_call: bool = request.get_json()["ongoing_call"]
    put_ongoing_call(Call(room, ongoing_call))
    return '', 201


@call_api_bp.route("/ongoing", methods=['GET'], endpoint="poll_ongoing_call")
def poll_ongoing_call():
    c: Optional[Call] = find_ongoing_call()
    if c:
        return jsonify(c.as_dict()), 200
    return '', 202
