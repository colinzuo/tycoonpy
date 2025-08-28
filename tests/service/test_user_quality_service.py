import logging

from hpyhrtbase.utils import StrUtil

from tycoonpy.service import UserQualityService

mod_logger = logging.getLogger(__name__)


class TestStatService:
    def test_get_user_quality_distribution_list(
        self, user_quality_service: UserQualityService
    ):
        mod_logger.debug("Enter")

        distribution_list = user_quality_service.get_user_quality_distribution_list()

        mod_logger.debug(f"distribution_list {StrUtil.pprint(distribution_list)}")

        assert len(distribution_list) >= 0

        mod_logger.debug("Leave")

    def test_temp(self, user_quality_service: UserQualityService):
        mod_logger.debug("Enter")

        mod_logger.debug("Leave")
