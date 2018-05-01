# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.conf import settings
import os



class CcmappConfig(AppConfig):
    name = 'ccmapp'
    def ready(self):
        upload_dir = settings.UPLOAD_DIR
        if not os.path.isdir(upload_dir):
            os.mkdir(upload_dir)

