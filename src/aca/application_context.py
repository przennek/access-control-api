import redis
from injector import inject, singleton
from redis import Redis

from aca.api.model.input.lock_control_input import LockControlModel
from aca.api.model.video_stream_model import VideoStreamModel
from aca.gpio.buzzer_driver import BuzzerDriver
from aca.gpio.lock_driver import LockDriver


# di context, default scope singleton
@inject
def context(binder):
    buzzer_driver = BuzzerDriver()
    binder.bind(BuzzerDriver, to=buzzer_driver, scope=singleton)

    lock_driver = LockDriver(buzzer_driver)
    binder.bind(LockDriver, to=lock_driver, scope=singleton)

    binder.bind(LockControlModel, to=LockControlModel(lock_driver), scope=singleton)

    binder.bind(VideoStreamModel, to=VideoStreamModel(), scope=singleton)

    binder.bind(Redis, redis.StrictRedis(host='app-redis-1', port=6379, db=0), scope=singleton)