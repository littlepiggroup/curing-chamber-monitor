import datetime

from ccmapp.samplemgr.update_samples import Sync
from ccmapp.videomgr import videomgr
import ccmapp.temperature_humidity_mgr.temphmdtymgr as TH
import collect_subscribe.collect_subscribe as CS
import logging


logger = logging.getLogger(__name__)


def update_samples_task():
    logger.info("update_samples_task triggered at " + str(datetime.datetime.now()))
    Sync().sync()
    logger.info("update_samples_task completed at " + str(datetime.datetime.now()))


def fetch_video_task():
    logger.info("fetch_video_task triggered at " + str(datetime.datetime.now()))
    videomgr.collect()
    logger.info("fetch_video_task completed at " + str(datetime.datetime.now()))


def send_alert_notification():
    logger.info("Start to send alert notification by scheduler.")
    CS.send_alert_short_message()
    logger.info("Complete sending alert notification by scheduler.")

def mock_temperature_humidity_data_generator():
    logger.info("Start to gen mock data")
    TH.gen_mock_data()
    logger.info("End gen mock data")



