from enum import Enum
from typing import Optional

from aca.api.db.dao.call_room_dao import CallControlDAO
from aca.api.db.dao.enrollment_dao import EnrollmentDAO
from aca.api.model.call import Call
from aca.api.service.server_audio_service import ServerAudioService


class CallResult(Enum):
    CREATED = "CREATED"
    ROOM_NOT_FOUND = "ROOM_NOT_FOUND"
    ANOTHER_ONGOING_CALL_IN_PROGRESS = "ANOTHER_ONGOING_CALL_IN_PROGRESS"


class CallControlService:
    number_not_found: str = "res/sounds/nie_ma_takiego_numeru.wav"

    def __init__(self, call_control_dao: CallControlDAO, enrollment_dao: EnrollmentDAO,
                 audio_service: ServerAudioService):
        self.call_control_dao = call_control_dao
        self.enrollment_dao = enrollment_dao
        self.audio_service = audio_service

    def create_call(self, call: Call) -> CallResult:
        if not self.enrollment_dao.exists(str(call.room)):
            self.audio_service.play(self.number_not_found, blocking=False)
            return CallResult.ROOM_NOT_FOUND

        created: bool = self.call_control_dao.put_ongoing_call(call)
        if created:
            return CallResult.CREATED
        else:
            return CallResult.ANOTHER_ONGOING_CALL_IN_PROGRESS

    def find_ongoing_call(self) -> Optional[Call]:
        return self.call_control_dao.find_ongoing_call()
