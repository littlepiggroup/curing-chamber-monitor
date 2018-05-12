# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.core.management.base import BaseCommand

from ccmapp.temperature_humidity_mgr.temphmdtymgr import collect_save_temperature_humidity_data
from ccmapp.videomgr.videomgr import collect


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch data for all sensors.'

    def handle(self, *args, **options):
        collect_save_temperature_humidity_data()
