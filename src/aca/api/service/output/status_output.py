from dataclasses import dataclass
from enum import Enum


class ServerStatus(Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


@dataclass
class StatusOutput:
    server_status: ServerStatus

    def as_dict(self):
        return {
            "server_status": self.server_status.value.__str__()
        }
