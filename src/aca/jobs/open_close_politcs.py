import logging
import time

import redis
from redis import Redis

from aca.api.db.dao.open_door_policy_dao import OpenDoorPolicyDAO
from aca.api.service.open_door_policy_service import OpenDoorPolicyService
from aca.gpio.buzzer_driver import BuzzerDriver
from aca.gpio.lock_driver import LockDriver

logger = logging.getLogger(__name__)
logging.basicConfig(level="INFO")

if __name__ == "__main__":
    strict_redis: Redis = redis.StrictRedis(host='app-redis-1', port=6379, db=0)
    model: OpenDoorPolicyService = OpenDoorPolicyService(OpenDoorPolicyDAO(strict_redis))
    driver = LockDriver(BuzzerDriver())

    for i in range(12):  # workaround for cron granularity
        policies = model.get_currently_active_policies()

        if policies:
            driver.open_lock(buzz=False)
        else:
            driver.close_lock(buzz=False)

        if i < 11:
            time.sleep(5)
