import redis
from injector import inject, singleton
from redis import Redis

from aca.api.db.dto.enrollment_dto import EnrollmentDTO
from aca.api.db.dto.open_door_policy_dto import OpenDoorPolicyDTO
from aca.api.model.lock_control_model import LockControlModel
from aca.api.model.open_door_policy_model import OpenDoorPolicyModel
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

    strict_redis = redis.StrictRedis(host='app-redis-1', port=6379, db=0)
    door_policy_dto = OpenDoorPolicyDTO(strict_redis)
    binder.bind(LockControlModel, to=LockControlModel(lock_driver, door_policy_dto),
                scope=singleton)

    binder.bind(VideoStreamModel, to=VideoStreamModel(), scope=singleton)

    binder.bind(Redis, strict_redis, scope=singleton)

    binder.bind(EnrollmentDTO, EnrollmentDTO(strict_redis), scope=singleton)

    binder.bind(OpenDoorPolicyDTO, door_policy_dto, scope=singleton)

    binder.bind(OpenDoorPolicyModel, OpenDoorPolicyModel(door_policy_dto), scope=singleton)
