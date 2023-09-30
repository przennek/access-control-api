import re
from typing import Optional

from redis import Redis

from aca.api.db.model.enrollment import Enrollment
from aca.api.db.redis import db_atomic_update


class EnrollmentDTO:

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
