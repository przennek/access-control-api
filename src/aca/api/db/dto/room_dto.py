import logging
import re
from typing import Optional

from redis import Redis

from aca.api.db.model.call import Call
from aca.api.db.redis import db_atomic_update
from aca.common.di import iocc

logger = logging.getLogger(__name__)


def find_ongoing_call() -> Optional[Call]:
    key_pattern = "call_room;*"
    redis: Redis = iocc(Redis)
    keys = redis.keys(key_pattern)
    keys_with_true_value = []

    for key in keys:
        value = redis.get(key)
        logger.info(value)
        logger.info(key)
        if value == b'True':
            room_match = re.match(r'call_room;(\d+);', key.decode())
            if room_match:
                keys_with_true_value.append(key.decode())

    if len(keys_with_true_value) == 0:
        return None
    if len(keys_with_true_value) == 1:
        value = keys_with_true_value[0].split(";")
        return Call(value[1], True)

    raise Exception("Multiple ongoing calls.")  # TODO more elegant exceptions and handlers


# Note to self. This is not thread safe, however since I have only one numeric pad which can
# be used only to perform a single call it shouldn't be a problem.
def put_ongoing_call(call: Call) -> bool:
    if find_ongoing_call() is None:
        db_atomic_update(call.get_key(), str(call.get_value()))
        return True
    return False
