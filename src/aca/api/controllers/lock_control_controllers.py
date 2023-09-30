import logging

from flask import Blueprint, request
from flask import jsonify

from aca.api.model.input.lock_control_input import LockControlInput
from aca.api.model.lock_control_model import LockControlModel
from aca.api.model.open_door_policy_model import OpenDoorPolicyModel
from aca.common.di import iocc
from aca.common.schema import validate_json_schema, lock_input_json_schema, \
    open_lock_policy_json_schema

lock_api_bp = Blueprint('lock_api', __name__, url_prefix='/api/lock')

logger = logging.getLogger(__name__)


@lock_api_bp.route('/control', methods=['POST'], endpoint="post_lock_control")
@validate_json_schema(lock_input_json_schema)
def post_lock_control():
    logger.debug("Handling POST /api/lock/control")
    lock_input: LockControlInput = LockControlInput(request.get_json())
    iocc(LockControlModel).handle_request(lock_input)
    return jsonify({'status': 'success'}), 200


@lock_api_bp.route('/policy', methods=['POST'], endpoint="post_open_lock_policy")
@validate_json_schema(open_lock_policy_json_schema)
def post_open_lock_policy():
    logger.debug("Handling POST /api/lock/policy")
    saved: bool = iocc(OpenDoorPolicyModel).create_policies(request.get_json())
    if saved:
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error'}), 400


@lock_api_bp.route('/policy', methods=['DELETE'], endpoint="delete_policy_by_id")
def delete_policy_by_id():
    logger.debug("Handling DELETE /api/lock/policy")
    uid = request.args.get('id')

    try:
        if uid:
            iocc(OpenDoorPolicyModel).delete(uid)
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
            iocc(OpenDoorPolicyModel).switch_state(uid, state)

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
        'policies': [policy.as_dict() for policy in iocc(OpenDoorPolicyModel).get_policies()]
    }), 200


@lock_api_bp.route('/policy/active', methods=['GET'], endpoint="get_active_open_lock_policy")
def get_active_open_lock_policy():
    logger.debug("Handling GET /api/lock/policy/active")
    return jsonify({
        'policies': [
            policy.as_dict() for policy in
            iocc(OpenDoorPolicyModel).get_currently_active_policies()
        ]
    }), 200
