import logging
import re
from typing import Optional

from redis import Redis

from aca.api.db.redis import db_atomic_update
from aca.api.model.enrollment import Enrollment

logger = logging.getLogger(__name__)

class EnrollmentDAO:

    def __init__(self, redis: Redis):
        self.redis: Redis = redis

    @staticmethod
    def create(enrollment: Enrollment) -> None:
        db_atomic_update(enrollment.get_key(), enrollment.get_value())

    def find(self, code: str) -> Optional[Enrollment]:
        key_pattern = "enrollment;*;"
        for key in self.redis.keys(key_pattern):
            saved_code = self.redis.get(key)
            if (saved_code == code.encode()
                    and re.match(r'enrollment;(\d+);', key.decode())):
                return Enrollment(code, int(key.decode().split(";")[1]))

        return None

    def exists(self, room: str):
        key = f"enrollment;" + room + ";"
        keys = [k.decode("UTF-8") for k in self.redis.keys("enrollment;*;")]
        return key in keys
