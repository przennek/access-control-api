import redis
from injector import inject, singleton
from redis import Redis

from aca.api.db.dao.call_room_dao import CallControlDAO
from aca.api.db.dao.enrollment_dao import EnrollmentDAO
from aca.api.db.dao.open_door_policy_dao import OpenDoorPolicyDAO
from aca.api.db.dao.pin_dao import PinDAO
from aca.api.service.call_control_service import CallControlService
from aca.api.service.lock_control_service import LockControlService
from aca.api.service.open_door_policy_service import OpenDoorPolicyService
from aca.api.service.pin_service import PinService
from aca.api.service.server_audio_service import ServerAudioService
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
    door_policy_dto = OpenDoorPolicyDAO(strict_redis)
    pin_dto = PinDAO(strict_redis)

    binder.bind(PinService, to=PinService(pin_dto), scope=singleton)

    binder.bind(Redis, strict_redis, scope=singleton)

    enrollment_dao = EnrollmentDAO(strict_redis)
    binder.bind(EnrollmentDAO, enrollment_dao, scope=singleton)

    binder.bind(OpenDoorPolicyDAO, door_policy_dto, scope=singleton)

    binder.bind(OpenDoorPolicyService, OpenDoorPolicyService(door_policy_dto), scope=singleton)

    audio_service = ServerAudioService()
    binder.bind(ServerAudioService, audio_service)

    binder.bind(LockControlService,
                to=LockControlService(lock_driver, door_policy_dto, pin_dto, audio_service),
                scope=singleton)

    call_control_dao = CallControlDAO(strict_redis)
    binder.bind(CallControlDAO, call_control_dao)

    binder.bind(CallControlService,
                CallControlService(call_control_dao, enrollment_dao, audio_service))
