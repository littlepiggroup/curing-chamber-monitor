# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.core.management.base import BaseCommand
from ccmapp.company_project_mgr import pull_company_project
from ccmapp.samplemgr.sample_alert_scanner import AlertScanner


class Command(BaseCommand):
    help = 'Sync project'

    def __init__(self):
        pass

    def handle(self, *args, **options):
        alert_scanner = AlertScanner()
        alert_scanner.scan()