import logging

from flask import Blueprint, request
from flask import jsonify

from aca.api.model.input.lock_control_input import LockControlInput, LockControlModel
from aca.api.model.output.status_output import ServerStatus, StatusOutput
from aca.common.di import iocc
from aca.common.schema import validate_json_schema, lock_input_json_schema

# Create a new Blueprint with a unique name and URL prefix
controller_bp = Blueprint('controller', __name__, url_prefix='/api')

logger = logging.getLogger(__name__)


@controller_bp.route('/server/status', methods=['GET'])
def get_server_status():
    logger.debug("Handling GET /api/server/status")
    return jsonify(StatusOutput(ServerStatus.ONLINE).as_dict()), 200


@controller_bp.route('/lock/control', methods=['POST'])
@validate_json_schema(lock_input_json_schema)
def post_lock_control():
    logger.debug("Handling POST /api/lock/control")
    lock_input: LockControlInput = LockControlInput(request.get_json())
    iocc(LockControlModel).handle_request(lock_input)
    return jsonify({'status': 'success'}), 200
