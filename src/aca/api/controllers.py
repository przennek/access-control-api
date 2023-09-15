import logging

from flask import Blueprint, request, render_template, Response
from flask import jsonify

from aca.api.model.audio_stream_model import AudioStreamModel
from aca.api.model.input.lock_control_input import LockControlInput, LockControlModel
from aca.api.model.output.status_output import ServerStatus, StatusOutput
from aca.api.model.video_stream_model import VideoStreamModel
from aca.common.di import iocc
from aca.common.schema import validate_json_schema, lock_input_json_schema

# Create a new Blueprint with a unique name and URL prefix
controller_bp = Blueprint('controller', __name__, url_prefix='/api', template_folder='templates')

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


@controller_bp.route("/view")
def serve_webpage():
    return render_template("controller/index.html")


@controller_bp.route('/stream/video_feed')
def video_feed():
    return Response(iocc(VideoStreamModel).generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@controller_bp.route("/stream/audio_feed")
def audio_feed():
    return Response(iocc(AudioStreamModel).generate(), mimetype="audio/x-wav;codec=pcm")
