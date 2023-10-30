from redis import Redis

from aca.api.db.model.pin import Pin


class PinDTO:

    def __init__(self, redis: Redis):
        self.redis: Redis = redis

    def add(self, pin: Pin) -> None:
        self.redis.sadd(pin.get_key(), pin.get_value())

    def exists(self, pin: Pin) -> bool:
        return self.redis.sismember(pin.get_key(), str(pin.get_value())) == 1

    def remove(self, pin: Pin) -> None:
        self.redis.srem(Pin.get_key(), pin.get_value())
