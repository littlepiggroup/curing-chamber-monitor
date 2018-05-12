# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.core.management.base import BaseCommand

from ccmapp.collect_subscribe.collect_subscribe import send_alert_short_message


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send alert notifications to phone.'

    def handle(self, *args, **options):
        send_alert_short_message()