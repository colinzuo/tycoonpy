import logging

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hpyhrtbase import hpyhrt_context
from hpyhrtbase.utils import TimeUtil

from tycoonpy.app.tycoon_app import tycoon_app_setup
from tycoonpy.controller import (
    user_quality_controller,
)
from tycoonpy.utils import ContextUtil

mod_logger = logging.getLogger(__name__)


def rest_app_setup() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    base_router = APIRouter(prefix="/tycoonpy-api")
    base_router.include_router(user_quality_controller.router)

    app.include_router(base_router)

    return app


def init_app_default_configs():
    config_inst = hpyhrt_context.get_config_inst()

    if not hasattr(config_inst, "http_server_port"):
        config_inst.http_server_port = 5000


def debug_main():
    user_quality_service = ContextUtil.get_user_quality_service()

    with TimeUtil.timeit() as ns:
        user_quality_service.get_user_quality_distribution_list()
    duration = ns.duration

    mod_logger.debug(f"Leave duration {duration:.3}")

if __name__ == "__main__":
    tycoon_app_setup("configs/tycoonpy.conf")

    config_inst = hpyhrt_context.get_config_inst()

    app = rest_app_setup()

    if False:
        debug_main()
    else:
        uvicorn.run(app, host="0.0.0.0", port=config_inst.http_server_port)
