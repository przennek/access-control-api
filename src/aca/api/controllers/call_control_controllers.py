import logging
from typing import Optional

from flask import Blueprint, request, jsonify

from aca.api.model.call import Call, CallStatus
from aca.api.service.call_control_service import CallControlService, CallResult
from aca.common.di import iocc
from aca.common.schema import validate_json_schema, call_room_json_schema

call_api_bp = Blueprint('call_api', __name__, url_prefix='/api/call')

logger = logging.getLogger(__name__)


@call_api_bp.route("", methods=['POST'], endpoint="call")
@validate_json_schema(call_room_json_schema)
def call():
    logger.debug("Handling POST /api/call")
    room: int = request.get_json()["room"]
    call_status: str = request.get_json()["call_status"]
    result: CallResult = iocc(CallControlService).create_call(
        Call(room, CallStatus.from_value(call_status)))

    if result == CallResult.CREATED:
        return '', 201

    if result == CallResult.ROOM_NOT_FOUND:
        return '', 404

    if result == CallResult.ANOTHER_ONGOING_CALL_IN_PROGRESS:
        return '', 412

    return '', 500


@call_api_bp.route("/ongoing", methods=['GET'], endpoint="poll_ongoing_call")
def poll_ongoing_call():
    c: Optional[Call] = iocc(CallControlService).find_ongoing_call()
    if c:
        return jsonify(c.as_dict()), 200

    return '', 202
