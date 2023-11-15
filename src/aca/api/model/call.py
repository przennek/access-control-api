from dataclasses import dataclass
from enum import Enum
from typing import Dict


class CallStatus(Enum):
    ANSWERED = "ANSWERED"
    NOT_ANSWERED = "NOT_ANSWERED"
    INACTIVE = "INACTIVE"

    @staticmethod
    def from_value(status):
        try:
            return CallStatus(status)
        except ValueError:
            return None

    def __str__(self):
        return self.value


@dataclass
class Call:
    room: int
    call_status: CallStatus

    def get_key(self) -> str:
        return f"call_room;{self.room};"

    def get_value(self) -> CallStatus:
        return self.call_status

    def as_dict(self) -> Dict[str, any]:
        return {
            "room": self.room,
            "call_status": str(self.call_status)
        }

    def is_ongoing(self) -> bool:
        return (self.get_value() == CallStatus.ANSWERED
                or self.get_value() == CallStatus.NOT_ANSWERED)
