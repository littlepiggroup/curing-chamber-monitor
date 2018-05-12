import thread

from ccmapp.videomgr.videomgr import VideoSchedulerThread
import logging
default_app_config = 'ccmapp.apps.CcmappConfig'
logger = logging.getLogger(__name__)


def startup():
    # print 'Start VideoSchedulerThread'
    # my_thread = VideoSchedulerThread()
    # my_thread.start()
    # print 'VideoSchedulerThread started.'
    pass

# startup() #TODO: enable it for collecting video. python manage.py runserver --noreload

# default_app_config = 'ccmapp.apps.CcmappConfig'
