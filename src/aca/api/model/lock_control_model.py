from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from injector import inject

from aca.api.db.dto.open_door_policy_dto import OpenDoorPolicyDTO
from aca.api.db.dto.pin_dto import PinDTO
from aca.api.db.model.open_door_policy import OpenDoorPolicy
from aca.api.db.model.pin import Pin
from aca.api.model.input.lock_control_input import Switch, LockControlInput
from aca.gpio.lock_driver import LockDriver


@dataclass
class LockControlModel:
    @inject
    def __init__(self, ld: LockDriver, open_dto: OpenDoorPolicyDTO, pin_dto: PinDTO):
        self.ld = ld
        self.open_dto = open_dto
        self.pin_dto = pin_dto

    def handle_request(self, lci: LockControlInput, pin: Optional[Pin]):
        {
            Switch.OPEN: lambda: self.open_lock(),
            Switch.CLOSE: lambda: self.ld.close_lock(),
            Switch.PIN_OPEN: lambda: self.pin_open(pin),
        }.get(lci.operation)()

    def pin_open(self, pin: Pin):
        if self.pin_dto.exists(pin):
            self.open_lock()

        raise Exception("Incorrect pin")  # TODO dedicated exceptions

    def open_lock(self):
        ttl_seconds = 20
        policy = OpenDoorPolicy.get_policy_from_now(timedelta_end=timedelta(seconds=ttl_seconds))
        self.open_dto.create(policy, ttl_seconds)
        self.ld.open_lock()
