# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ccm.ccmapp.models import Project, Sample, SampleAlert
from django.db.models import Q
import datetime

class AlertScanner(object):
    def __init__(self):
        pass
    def scan(self):
        #TODO: only scan in-progress projects
        projects = Project.objects.all()
        for proj in projects:
            samples = Sample.objects.filter(project=proj.id)
            for sample in samples:
                if sample.isAlert():
                    #Check SampleAlertTabe
                    self.update_or_create_alert(sample)

    def update_or_create_alert(self, sample):
        result = SampleAlert.objects.filter(
            Q(sample=sample.id) &
            (Q(status=SampleAlert.CREATED) | Q(status=SampleAlert.FIXING))
        )
        if len(result) == 1:
            # One corresponding is open. Just update time
            pass
        elif len(result) == 0:
            # Need new one alert
            pass
            now_datetime = datetime.datetime.now()
            new_alert = SampleAlert(sample=sample,
                                    create_time=now_datetime,
                                    created_by = 'system',
                                    update_time =now_datetime,
                                    updated_by = 'system',
                                    status = SampleAlert.CREATED
                                    )
            new_alert.save()
        else:
            # TODO: should be a internal error
            pass



