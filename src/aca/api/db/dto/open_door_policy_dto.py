import uuid
from datetime import time
from typing import List, Optional

from redis import Redis

from aca.api.db.model.open_door_policy import OpenDoorPolicy, Day
from aca.api.db.redis import db_atomic_update


class OpenDoorPolicyDTO:

    def __init__(self, redis: Redis):
        self.redis: Redis = redis

    @staticmethod
    def create(open_door_policy: OpenDoorPolicy, ttl_seconds: Optional[int] = None) -> None:
        db_atomic_update(open_door_policy.get_key(), open_door_policy.get_value(), ttl_seconds)

    def find(self) -> List[OpenDoorPolicy]:  # TODO (low) HMSET?
        key_pattern = "open_door_policy;*;*;*;*;"
        out = []
        for key in self.redis.keys(key_pattern):
            active = self.redis.get(key).decode().lower() == 'true'
            split = key.decode().split(";")
            _id: uuid.UUID = uuid.UUID(split[1])
            day: str = split[2]
            start_date_iso: time = time.fromisoformat(split[3])
            end_date_iso: time = time.fromisoformat(split[4])
            out.append(
                OpenDoorPolicy(_id, Day.from_value(day), start_date_iso, end_date_iso, active))

        return out

    def delete(self, uid: uuid.UUID):
        key_pattern = f"open_door_policy;{uid};*;*;*;"
        for key in self.redis.keys(key_pattern):
            self.redis.delete(key)

    def switch_state(self, uid: uuid.UUID, state: bool):
        key_pattern = f"open_door_policy;{uid};*;*;*;"
        for key in self.redis.keys(key_pattern):
            db_atomic_update(key, str(state))
