import logging

from flask import Blueprint, request
from flask import jsonify

from aca.api.model.pin import Pin
from aca.api.service.input.lock_control_input import LockControlInput
from aca.api.service.lock_control_service import LockControlService, PinOpenResult
from aca.api.service.open_door_policy_service import OpenDoorPolicyService
from aca.api.service.pin_service import PinService
from aca.common.di import iocc
from aca.common.schema import validate_json_schema, lock_input_json_schema, \
    open_lock_policy_json_schema, pin_json_schema

lock_api_bp = Blueprint('lock_api', __name__, url_prefix='/api/lock')

logger = logging.getLogger(__name__)


@lock_api_bp.route('/control', methods=['POST'], endpoint="post_lock_control")
@validate_json_schema(lock_input_json_schema)
def post_lock_control():
    logger.debug("Handling POST /api/lock/control")
    lock_input: LockControlInput = LockControlInput(request.get_json())
    iocc(LockControlService).handle_request(lock_input)
    return jsonify({'status': 'success'}), 200


@lock_api_bp.route('/pin', methods=['POST'], endpoint="pin_open_lock")
@validate_json_schema(pin_json_schema)
def post_pin_control():
    logger.debug("Handling POST /api/lock/pin")
    lock_input: LockControlInput = LockControlInput({
        "operation": "PIN_OPEN",
        "buzzer_duration_seconds": 2
    })
    pin = Pin(request.get_json()["pin"])

    result: PinOpenResult = iocc(LockControlService).handle_request(lock_input, pin)
    if result == PinOpenResult.INVALID_PIN:
        return jsonify({'status': 'invalid_pin'}), 403

    if (result == PinOpenResult.OPENED or result == PinOpenResult.CLOSED
            or result == PinOpenResult.IDK):
        return jsonify({'status': 'success'}), 200

    return '', 500


@lock_api_bp.route('/pin/create', methods=['POST'], endpoint="pin_create")
@validate_json_schema(pin_json_schema)
def post_pin_create():
    logger.debug("Handling POST /api/lock/pin/create")
    pin = Pin(request.get_json()["pin"])
    iocc(PinService).create(pin)
    return jsonify({'status': 'success'}), 200


@lock_api_bp.route('/pin/delete', methods=['DELETE'], endpoint="pin_delete")
@validate_json_schema(pin_json_schema)
def post_pin_delete():
    logger.debug("Handling DELETE /api/lock/pin/delete")
    pin = Pin(request.get_json()["pin"])
    iocc(PinService).remove(pin)
    return jsonify({'status': 'success'}), 204


@lock_api_bp.route('/policy', methods=['POST'], endpoint="post_open_lock_policy")
@validate_json_schema(open_lock_policy_json_schema)
def post_open_lock_policy():
    logger.debug("Handling POST /api/lock/policy")
    saved: bool = iocc(OpenDoorPolicyService).create_policies(request.get_json())
    if saved:
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error'}), 400


@lock_api_bp.route('/policy', methods=['DELETE'], endpoint="delete_policy_by_id")
def delete_policy_by_id():
    logger.debug("Handling DELETE /api/lock/policy")
    uid = request.args.get('id')

    try:
        if uid:
            iocc(OpenDoorPolicyService).delete(uid)
        return jsonify({'status': 'success'}), 200
    except ValueError as e:
        logger.error(f"Error while trying to delete the policy id: {uid}", e)

    return jsonify({'status': 'Bad Request, a valid id UUID string is required'}), 400


@lock_api_bp.route('/policy', methods=['PUT'], endpoint="switch_policy_state_by_id")
def switch_policy_state_by_id():
    logger.debug("Handling PUT /api/lock/policy")
    uid = request.args.get('id')

    try:
        state = request.args.get('state').lower() == 'true'
        if uid:
            iocc(OpenDoorPolicyService).switch_state(uid, state)

        return jsonify({'status': 'success'}), 200
    except ValueError:
        logger.error(f"Error while trying to switch the policy id: {uid}", e)

    return jsonify(
        {'status': 'Bad Request, a valid id UUID string and a state boolean is required'}
    ), 400


@lock_api_bp.route('/policy', methods=['GET'], endpoint="get_open_lock_policy")
def get_open_lock_policy():
    logger.debug("Handling GET /api/lock/policy")
    return jsonify({
        'policies': [policy.as_dict() for policy in iocc(OpenDoorPolicyService).get_policies()]
    }), 200


@lock_api_bp.route('/policy/active', methods=['GET'], endpoint="get_active_open_lock_policy")
def get_active_open_lock_policy():
    logger.debug("Handling GET /api/lock/policy/active")
    return jsonify({
        'policies': [
            policy.as_dict() for policy in
            iocc(OpenDoorPolicyService).get_currently_active_policies()
        ]
    }), 200
