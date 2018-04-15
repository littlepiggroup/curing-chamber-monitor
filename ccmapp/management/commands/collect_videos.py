# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.core.management.base import BaseCommand
from ccmapp.videomgr.videomgr import collect


logger = logging.getLogger("samples.sync")


class Command(BaseCommand):
    help = 'Fetch live stream for every camera and save as MP4 file.'

    def handle(self, *args, **options):
        collect()
