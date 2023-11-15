from dataclasses import dataclass

from aca.api.db.dao.pin_dao import PinDAO
from aca.api.model.pin import Pin


@dataclass
class PinService:
    pin_dto: PinDAO

    def create(self, pin: Pin):
        self.pin_dto.add(pin)

    def remove(self, pin: Pin):
        self.pin_dto.remove(pin)
