import logging

from hpyhrtbase import hpyhrt_context

import tycoonpy.model.po  # noqa: F401
from tycoonpy.model.po.database import setup_database
from tycoonpy.service import (
    UserQualityService,
)

mod_logger = logging.getLogger(__name__)


def data_app_setup() -> None:
    global_context = hpyhrt_context.get_global_context()

    config_inst = hpyhrt_context.get_config_inst()

    if not hasattr(config_inst, "db_url"):
        raise Exception("db_url not set")

    setup_database(config_inst.db_url)

    user_quality_service = UserQualityService()

    global_context.user_quality_service = user_quality_service
