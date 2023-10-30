from dataclasses import dataclass
from enum import Enum


class Switch(Enum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    PIN_OPEN = "PIN_OPEN"


class LockControlInput:
    operation: Switch
    buzzer_duration_seconds: int

    def __init__(self, data):
        self.operation = Switch[data["operation"]]
        self.buzzer_duration_seconds = data.get("buzzer_duration_seconds")
