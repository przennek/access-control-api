from typing import Optional

from redis import Redis

from aca.common.di import iocc


def db_atomic_update(key: str, value: str) -> None:
    # Try to SET the key if it doesn't exist (atomic operation)
    # SETNX returns 1 if the key was set, 0 if the key already exists
    redis: Redis = iocc(Redis)
    setnx = redis.setnx(key, value)

    if setnx != 1:
        # The key already exists, so use GETSET to atomically GET and SET a new value
        redis.getset(key, value)


def db_get(key: str) -> Optional[any]:
    redis: Redis = iocc(Redis)
    return redis.get(key)
