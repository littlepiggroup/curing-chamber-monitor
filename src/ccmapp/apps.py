# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.conf import settings
import os
import logging
import thread
import time
logger = logging.getLogger()



class CcmappConfig(AppConfig):
    name = 'ccmapp'
    def ready(self):
        import sys
        import ccmapp.temperature_humidity_mgr.collect_server as CS
        logger.info(sys.argv)
        is_start_server = True
        if len(sys.argv) > 1:
            django_cmd = sys.argv[1]
            logger.info('Django cmd: %s' % django_cmd)
            if django_cmd in ['crontab', 'collect_videos']:
                logger.info('Not start server for crontab,collect_videos')
                is_start_server = False
        if is_start_server:
            logger.info('Start socket server.')
            # thread.start_new_thread(CS.start_server, ())
            thread.start_new_thread(CS.start_twisted_server, ())
            logger.info('Sleep 3 seconds to let socket server up')
            time.sleep(3)

        upload_dir = settings.UPLOAD_DIR
        if not os.path.isdir(upload_dir):
            os.mkdir(upload_dir)
        logger.info('Ready!')

