import logging

from hpyhrtbase import init_app_base

from tycoonpy.app.data_app import data_app_setup

mod_logger = logging.getLogger(__name__)


def tycoon_app_setup(config_file: str = "configs/tycoonpy.conf") -> None:
    init_app_base.init_app_base(
        config_file, None, check_dir_names=["src", "tests"]
    )

    data_app_setup()

    mod_logger.info("Leave")
