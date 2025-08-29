import logging

from tycoonpy.app.tycoon_app import tycoon_app_setup

mod_logger = logging.getLogger(__name__)

def meeting_record_import():
    mod_logger.info("Enter")

    mod_logger.info("Leave")

if __name__ == "__main__":
    tycoon_app_setup()

    meeting_record_import()
