from __future__ import annotations

from typing import TYPE_CHECKING

from hpyhrtbase import hpyhrt_context

if TYPE_CHECKING:
    from tycoonpy.service import (
        UserQualityService,
    )


class ContextUtil:
    @staticmethod
    def get_user_quality_service() -> UserQualityService:
        global_context = hpyhrt_context.get_global_context()
        return global_context.user_quality_service
