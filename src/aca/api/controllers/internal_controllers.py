import logging
from flask import Blueprint, send_from_directory

api_bp = Blueprint('api', __name__, url_prefix='/')

logger = logging.getLogger(__name__)


@api_bp.route('/static/aca-front')
@api_bp.route('/static/aca-front/')
def serve_index():
    return send_from_directory('static', 'index.html')
