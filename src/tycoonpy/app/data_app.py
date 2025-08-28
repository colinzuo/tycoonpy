import logging

from hpyhrtbase import hpyhrt_context

from tycoonpy.service import (
    UserQualityService,
)

mod_logger = logging.getLogger(__name__)


def data_app_setup() -> None:
    global_context = hpyhrt_context.get_global_context()

    user_quality_service = UserQualityService()

    global_context.user_quality_service = user_quality_service
