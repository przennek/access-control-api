import logging

from flask import Blueprint

from aca.api.service.server_audio_service import ServerAudioService
from aca.common.di import iocc

audio_api_bp = Blueprint('audio_api', __name__, url_prefix='/api/audio')

logger = logging.getLogger(__name__)


@audio_api_bp.route('/play/beep', methods=['POST'], endpoint="play_beep")
def play_beep():
    logger.debug("Handling POST /api/audio/beep")
    iocc(ServerAudioService).play("res/sounds/beep.wav")
    return '', 200


@audio_api_bp.route('/play/peep', methods=['POST'], endpoint="play_peep")
def play_peep():
    logger.debug("Handling POST /api/audio/peep")
    iocc(ServerAudioService).play("res/sounds/peep.wav", blocking=False)
    iocc(ServerAudioService).play("res/sounds/peep.wav", blocking=False)
    return '', 200
