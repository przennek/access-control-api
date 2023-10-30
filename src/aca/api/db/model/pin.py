from dataclasses import dataclass
from typing import Dict


@dataclass
class Pin:
    value: int

    @staticmethod
    def get_key() -> str:
        return f"pin"

    def get_value(self) -> int:
        return self.value

    def as_dict(self) -> Dict[str, any]:
        return {
            "pin": self.value
        }
