import datetime

from ccm.ccmapp.samplemgr.update_samples import Sync
import logging

logger = logging.getLogger(__name__)


def update_samples_task():
    logger.info("update_samples_task triggered at " + str(datetime.datetime.now()))
    Sync().sync()
    logger.info("update_samples_task completed at " + str(datetime.datetime.now()))


