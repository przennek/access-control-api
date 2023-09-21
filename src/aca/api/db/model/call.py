from dataclasses import dataclass
from typing import Dict


@dataclass
class Call:
    room: int
    ongoing: bool

    def get_key(self) -> str:
        return f"call_room;{self.room};"

    def get_value(self) -> bool:
        return self.ongoing

    def as_dict(self) -> Dict[str, any]:
        return {
            "room": self.room,
            "ongoing_call": self.ongoing
        }
