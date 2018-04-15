# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.core.management.base import BaseCommand
from ccmapp.samplemgr.update_samples import Sync


logger = logging.getLogger("samples.sync")


class Command(BaseCommand):
    help = 'Sync samples into DB'

    def __init__(self):
        self.sync = Sync()

    def handle(self, *args, **options):
        self.sync.sync()
