import logging
import re
from typing import Optional

from redis import Redis

from aca.api.db.redis import db_atomic_update
from aca.api.model.call import Call, CallStatus

logger = logging.getLogger(__name__)


class CallControlDAO:

    def __init__(self, redis: Redis):
        self.redis = redis

    def find_ongoing_call(self) -> Optional[Call]:
        key_pattern = "call_room;*"
        keys = self.redis.keys(key_pattern)
        keys_with_true_value = []
        values = []

        for key in keys:
            value = self.redis.get(key)
            if value == b'ANSWERED' or value == b'NOT_ANSWERED':
                room_match = re.match(r'call_room;(\d+);', key.decode())
                if room_match:
                    keys_with_true_value.append(key.decode())
                    values.append(value)

        if len(keys_with_true_value) == 0:
            return None

        if len(keys_with_true_value) == 1:
            value = keys_with_true_value[0].split(";")
            return Call(value[1], CallStatus.from_value(values[0].decode("UTF-8")))

        raise Exception("Multiple ongoing calls.")  # TODO more elegant exceptions and handlers

    # Note to self. This is not thread safe, however since I have only one numeric pad which can
    # be used only to perform a single call it shouldn't be a problem.
    def put_ongoing_call(self, call: Call) -> bool:
        call_expire_seconds: int = 900
        ongoing_call = self.find_ongoing_call()
        if self._should_accept_call(call, ongoing_call):
            db_atomic_update(
                key=call.get_key(),
                value=str(call.get_value()),
                ttl_seconds=call_expire_seconds
            )
            return True

        return False

    @staticmethod
    def _should_accept_call(call: Call, ongoing_call: Optional[Call]) -> bool:
        return (
                # cancelling the call
                not call.is_ongoing()
                # no ongoing calls, a new ongoing call created
                or (call.is_ongoing() and ongoing_call is None)
                # updating the status of ongoing call to answered
                or (ongoing_call is not None and call.call_status == CallStatus.ANSWERED
                    and ongoing_call.call_status == CallStatus.NOT_ANSWERED)  #
        )
