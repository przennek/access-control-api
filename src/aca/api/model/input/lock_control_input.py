from enum import Enum


class Switch(Enum):
    OPEN = "OPEN"
    CLOSE = "CLOSE"


class LockControlInput:
    operation: Switch
    buzzer_duration_seconds: int

    def __init__(self, data):
        self.operation = Switch[data["operation"]]
        self.buzzer_duration_seconds = data.get("buzzer_duration_seconds")
