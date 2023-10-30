from dataclasses import dataclass

from aca.api.db.dto.pin_dto import PinDTO
from aca.api.db.model.pin import Pin


@dataclass
class PinModel:
    pin_dto: PinDTO

    def create(self, pin: Pin):
        self.pin_dto.add(pin)

    def remove(self, pin: Pin):
        self.pin_dto.remove(pin)
