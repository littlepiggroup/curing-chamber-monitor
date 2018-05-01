import datetime

from ccmapp.samplemgr.update_samples import Sync
from ccmapp.videomgr import videomgr
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
    CS.send_alert_short_message()
