import logging
import time
from typing import Optional

import redis
from redis import Redis

from aca.api.db.dao.call_room_dao import CallControlDAO
from aca.api.db.dao.enrollment_dao import EnrollmentDAO
from aca.api.model.call import Call, CallStatus
from aca.api.service.call_control_service import CallControlService
from aca.api.service.server_audio_service import ServerAudioService

logger = logging.getLogger(__name__)
logging.basicConfig(level="INFO")

if __name__ == "__main__":
    import os
    os.chdir("/app")

    logger.info("Calling noise job.")
    strict_redis: Redis = redis.StrictRedis(host='app-redis-1', port=6379, db=0)
    audio_service: ServerAudioService = ServerAudioService()
    model: CallControlService = CallControlService(
        call_control_dao=CallControlDAO(redis=strict_redis),
        enrollment_dao=EnrollmentDAO(redis=strict_redis),
        audio_service=audio_service
    )
    beep: str = "res/sounds/beep.wav"
    for i in range(13):  # workaround for cron granularity
        # audio is 4,48 s. There will be 1760 ms delay.
        call: Optional[Call] = model.find_ongoing_call()

        if call is not None and call.call_status == CallStatus.NOT_ANSWERED:
            audio_service.play(beep)
        else:
            time.sleep(4.615)
