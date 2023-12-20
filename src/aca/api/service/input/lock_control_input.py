from enum import Enum
from typing import Optional


class Switch(Enum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    PIN_OPEN = "PIN_OPEN"


class LockControlInput:
    operation: Switch
    open_duration_seconds: Optional[int]
    buzzer_duration_seconds: Optional[int]

    def __init__(self, data):
        self.operation = Switch[data["operation"]]
        self.buzzer_duration_seconds = data.get("buzzer_duration_seconds")
        self.open_duration_seconds = data.get("open_duration_seconds")
