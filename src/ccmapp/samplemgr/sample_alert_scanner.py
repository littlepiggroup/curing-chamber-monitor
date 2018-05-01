# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ccmapp.models import Project, Sample, SampleAlert, sample_is_alert
from django.db.models import Q
from datetime import datetime

import logging

logger = logging.getLogger(__name__)


class AlertScanner(object):
    def __init__(self):
        pass

    def scan(self):
        #TODO: only scan in-progress projects
        projects = Project.objects.all()
        for proj in projects:
            samples = Sample.objects.filter(project=proj.id)
            for sample in samples:
                if sample_is_alert(sample):
                    logger.debug("Got bad sample: %s", sample.id)
                    #Check SampleAlertTabe
                    self.update_or_create_alert(sample)

    def update_or_create_alert(self, sample):
        open_alerts = SampleAlert.objects.filter(
            Q(sample=sample.id) &
            (Q(status=SampleAlert.CREATED) | Q(status=SampleAlert.FIXING))
        )

        if len(open_alerts) == 1:
            # One corresponding is open. Just update time
            logger.debug("Update Alert for sample:%s", sample.id)

            sample_alert = open_alerts[0]
            sample_alert.update_time = datetime.now()
            sample_alert.save()
        elif len(open_alerts) == 0:
            # Need new one alert
            logger.debug("Create Alert for sample:%s", sample.id)
            now_datetime = datetime.now()
            new_alert = SampleAlert(sample=sample,
                                    create_time=now_datetime,
                                    update_time=now_datetime,
                                    status=SampleAlert.CREATED
                                    )
            new_alert.save()
        else:
            # TODO: should be a internal error
            pass



