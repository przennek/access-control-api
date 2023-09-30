import uuid
from dataclasses import dataclass
from datetime import time, datetime, timedelta
from enum import Enum
from typing import Dict, List


class Day(Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

    @staticmethod
    def from_value(day_str):
        try:
            return Day(day_str)
        except ValueError:
            return None

    def __str__(self):
        return self.value


@dataclass
class OpenDoorPolicy:
    id: uuid.UUID
    day: Day
    start_time: time
    end_time: time
    active: bool

    def get_key(self) -> str:
        return (f"open_door_policy;{self.id};{self.day};{self.start_time.isoformat()};"
                f"{self.end_time.isoformat()};")

    def get_value(self) -> str:
        return str(self.active)

    def as_dict(self) -> Dict[str, str]:
        return {
            "id": self.id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "day": self.day.value,
            "active": self.get_value()
        }

    @classmethod
    def get_policy_from_now(cls, timedelta_end: timedelta):
        today = datetime.now().date()
        current_time = datetime.now().time()
        end_time = (datetime.combine(today, current_time) + timedelta_end).time()

        return cls(
            uuid.uuid4(),
            Day(datetime.now().strftime('%A').upper()),
            current_time,
            end_time,
            True
        )


def create_open_door_policies(data) -> List[OpenDoorPolicy]:
    return [
        OpenDoorPolicy(
            odp["id"] if odp["id"] is not None else uuid.uuid4(),
            odp["day"],
            time.fromisoformat(odp["start_time"]),
            time.fromisoformat(odp["end_time"]),
            odp["active"]
        ) for odp in data
    ]
