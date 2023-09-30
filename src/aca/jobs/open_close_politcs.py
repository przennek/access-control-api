import logging
import time

import redis
from redis import Redis

from aca.api.db.dto.open_door_policy_dto import OpenDoorPolicyDTO
from aca.api.model.open_door_policy_model import OpenDoorPolicyModel
from aca.gpio.buzzer_driver import BuzzerDriver
from aca.gpio.lock_driver import LockDriver

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    strict_redis: Redis = redis.StrictRedis(host='app-redis-1', port=6379, db=0)
    model: OpenDoorPolicyModel = OpenDoorPolicyModel(OpenDoorPolicyDTO(strict_redis))
    driver = LockDriver(BuzzerDriver())

    for i in range(12):  # workaround for cron granularity
        policies = model.get_currently_active_policies()

        if policies:
            driver.open_lock(buzz=False)
        else:
            driver.close_lock(buzz=False)

        if i < 11:
            time.sleep(5)
