import logging

from flask import Blueprint, Response

from aca.api.model.audio_stream_model import AudioStreamModel
from aca.api.model.video_stream_model import VideoStreamModel
from aca.common.di import iocc

media_api_bp = Blueprint('media_api', __name__, url_prefix='/api/stream')

logger = logging.getLogger(__name__)


@media_api_bp.route('/video_feed', endpoint="video_feed")
def video_feed():
    return Response(iocc(VideoStreamModel).generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@media_api_bp.route("/audio_feed", endpoint="audio_feed")
def audio_feed():
    return Response(iocc(AudioStreamModel).generate(), mimetype="audio/x-wav;codec=pcm")
