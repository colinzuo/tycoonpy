from __future__ import annotations

import logging

mod_logger = logging.getLogger(__name__)

class UserQualityService:
    def __init__(
        self,
    ):
        pass

    def get_user_quality_distribution_list(
        self,
    ) -> list[dict]:
        mod_logger.debug("Enter")

        return [
            {
                "A": 32,
            },
            {
                "B": 45,
            },
            {
                "C": 23,
            },
        ]
