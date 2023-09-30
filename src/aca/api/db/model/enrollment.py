from dataclasses import dataclass
from typing import Dict


@dataclass
class Enrollment:
    code: str
    room: int

    def get_key(self) -> str:
        return f"enrollment;{self.room};"

    def get_value(self) -> str:
        return self.code

    def as_dict(self) -> Dict[str, str]:
        return {
            "room": self.room,
            "code": self.code
        }
