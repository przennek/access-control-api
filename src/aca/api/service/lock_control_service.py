import threading
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum
from typing import Optional

from flask import current_app
from injector import inject

from aca.api.db.dao.open_door_policy_dao import OpenDoorPolicyDAO
from aca.api.db.dao.pin_dao import PinDAO
from aca.api.model.open_door_policy import OpenDoorPolicy
from aca.api.model.pin import Pin
from aca.api.service.input.lock_control_input import LockControlInput, Switch
from aca.api.service.server_audio_service import ServerAudioService
from aca.gpio.lock_driver import LockDriver


class PinOpenResult(Enum):
    OPENED = "OPENED"
    CLOSED = "CLOSED"
    INVALID_PIN = "INVALID_PIN"
    IDK = "IDK"  # threading...


@dataclass
class LockControlService:
    bad_pin: str = "res/sounds/bledny_kod.wav"
    door_opened: str = "res/sounds/drzwi_otwarte.wav"

    @inject
    def __init__(self, ld: LockDriver,
                 open_dto: OpenDoorPolicyDAO,
                 pin_dto: PinDAO,
                 audio_service: ServerAudioService):
        self.ld = ld
        self.open_dto = open_dto
        self.pin_dto = pin_dto
        self.audio_service = audio_service

    def handle_request(self, lci: LockControlInput, pin: Optional[Pin] = None) -> PinOpenResult:
        return {
            Switch.OPEN: lambda: self.open_lock(),
            Switch.CLOSE: lambda: self.ld.close_lock(),
            Switch.PIN_OPEN: lambda: self.pin_open(pin),
        }.get(lci.operation)()

    def close_lock(self) -> PinOpenResult:
        self.ld.close_lock()
        return PinOpenResult.CLOSED

    def pin_open(self, pin: Pin) -> PinOpenResult:
        context = current_app.app_context

        def _spawn_task():
            with context():
                if self.pin_dto.exists(pin):
                    self.open_lock()
                    self.audio_service.play(self.door_opened, blocking=False)
                else:
                    self.audio_service.play(self.bad_pin, blocking=False)

        threading.Thread(target=_spawn_task).start()
        return PinOpenResult.IDK

    def open_lock(self) -> PinOpenResult:
        ttl_seconds = 20
        policy = OpenDoorPolicy.get_policy_from_now(timedelta_end=timedelta(seconds=ttl_seconds))
        self.open_dto.create(policy, ttl_seconds)
        self.ld.open_lock()
        return PinOpenResult.OPENED
