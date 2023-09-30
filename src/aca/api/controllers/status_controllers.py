import logging

from flask import Blueprint, jsonify

from aca.api.model.output.status_output import ServerStatus, StatusOutput

status_api_bp = Blueprint('status_api', __name__, url_prefix='/api/status')

logger = logging.getLogger(__name__)


@status_api_bp.route('/server', methods=['GET'], endpoint="get_server_status")
def get_server_status():
    logger.debug("Handling GET /api/server/status")
    return jsonify(StatusOutput(ServerStatus.ONLINE).as_dict()), 200
