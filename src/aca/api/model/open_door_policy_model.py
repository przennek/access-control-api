import logging
import uuid
from dataclasses import dataclass
from datetime import timedelta
from typing import List

from aca.api.db.dto.open_door_policy_dto import OpenDoorPolicyDTO
from aca.api.db.model.open_door_policy import OpenDoorPolicy, create_open_door_policies

logger = logging.getLogger(__name__)


@dataclass
class OpenDoorPolicyModel:
    dto: OpenDoorPolicyDTO

    def create_policies(self, data) -> bool:
        try:
            open_door_policies: List[OpenDoorPolicy] = create_open_door_policies(data)
            for policy in open_door_policies:
                self.dto.create(policy)
        except Exception as e:
            logger.error(f"Error while trying to save open door policies.", e)
            return False

        return True

    def switch_state(self, uid: uuid.UUID, state: bool):
        self.dto.switch_state(uid, state)

    def delete(self, uid: uuid.UUID):
        self.dto.delete(uid)

    def get_policies(self) -> List[OpenDoorPolicy]:
        open_door_policies: List[OpenDoorPolicy] = self.dto.find()
        return open_door_policies

    def get_currently_active_policies(self) -> List[OpenDoorPolicy]:
        dummy_policy: OpenDoorPolicy = OpenDoorPolicy.get_policy_from_now(
            timedelta_end=timedelta()
        )

        matching_policies: List[OpenDoorPolicy] = [
            policy for policy in self.get_policies()
            if policy.day == dummy_policy.day
            and policy.start_time <= dummy_policy.start_time <= policy.end_time
            and policy.active
        ]

        return matching_policies
