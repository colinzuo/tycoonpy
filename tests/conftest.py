import os

import pytest
from hpyhrtbase import hpyhrt_context, init_app_base

from tycoonpy.service import (
    UserQualityService,
)


class RunContextBase:
    def __init__(self):
        self.config_inst = hpyhrt_context.get_config_inst()
        self.global_context = hpyhrt_context.get_global_context()


@pytest.fixture
def run_context_base(init_app):
    _run_context_base = RunContextBase()
    yield _run_context_base


@pytest.fixture(scope="session")
def root_dir() -> str:
    cur_file_dir = os.path.dirname(__file__)
    return cur_file_dir


@pytest.fixture(scope="session")
def configs_dir(root_dir) -> str:
    target = os.path.join(root_dir, "configs")
    return target


@pytest.fixture
def init_app(configs_dir):
    config_file = os.path.join(configs_dir, "tycoonpy_test.conf")
    init_app_base.init_app_base(config_file, check_dir_names=["src", "tests"])
    yield
    init_app_base.reset()
    hpyhrt_context.reset()


@pytest.fixture
def user_quality_service(init_app):
    service = UserQualityService()
    return service
