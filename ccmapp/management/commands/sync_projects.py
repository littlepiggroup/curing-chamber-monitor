# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.core.management.base import BaseCommand

from ccmapp.samplemgr.update_projects import getPrjInfo1


class Command(BaseCommand):
    help = 'Sync projects into DB'

    def __init__(self):
        pass

    def handle(self, *args, **options):
        getPrjInfo1()