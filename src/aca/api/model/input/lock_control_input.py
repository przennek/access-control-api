from dataclasses import dataclass
from enum import Enum

from injector import inject

from aca.gpio.lock_driver import LockDriver


class Switch(Enum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"


class LockControlInput:
    operation: Switch
    buzzer_duration_seconds: int

    def __init__(self, data):
        self.operation = Switch[data["operation"]]
        self.buzzer_duration_seconds = data.get("buzzer_duration_seconds")


@dataclass
class LockControlModel:
    @inject
    def __init__(self, ld: LockDriver):
        self.ld = ld

    def handle_request(self, lci: LockControlInput):
        {
            Switch.OPEN: lambda: self.ld.open_lock(),
            Switch.CLOSE: lambda: self.ld.close_lock()
        }.get(lci.operation)()
        # TODO add buzzer
