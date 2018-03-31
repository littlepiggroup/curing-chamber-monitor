# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class BuildingCompany(models.Model):
    instance_id = models.CharField(max_length=100, unique=True, null=True)
    name = models.CharField(max_length=100, unique=True)
    disabled = models.BooleanField(default=False)
    added_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-added_time',)


class BuildingCompanyUser(models.Model):
    instance_id = models.CharField(max_length=100, unique=True, null=True)
    login_name = models.CharField(max_length=100, unique=True)
    building_company = models.ForeignKey(BuildingCompany, related_name='users', null=True)
    disabled = models.BooleanField(default=False)
    added_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-added_time',)


class Project(models.Model):
    instance_id = models.CharField(max_length=100, unique=True, null=True)
    nature = models.CharField(max_length=20, null=True)
    num = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=256, null=True)
    status = models.IntegerField(null=True)
    create_time = models.DateTimeField(null=True)
    last_edit_time = models.DateTimeField(null=True)
    building_company = models.ForeignKey(BuildingCompany, related_name='projects')
    added_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-added_time',)


class ProjectName(models.Model):
    name = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey(Project, related_name='names')
    added_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-added_time', )


class Contract(models.Model):
    sign_number = models.CharField(max_length=100, unique=True)
    serial_num = models.CharField(max_length=100)
    project = models.ForeignKey(Project, related_name='contracts', db_column='project_id')
    checked_date_time = models.DateTimeField()
    checked = models.BooleanField()
    added_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-sign_number',)


class Sample(models.Model):
    instance_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    num = models.CharField(max_length=100)
    item_id = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    # project = models.ForeignKey(Project, related_name='project_id')
    contract = models.ForeignKey(Contract, related_name='+')
    count = models.IntegerField()
    status = models.IntegerField()
    status_str = models.CharField(max_length=20)
    regular = models.BooleanField()
    kind_id = models.CharField(max_length=100)
    kind_name = models.CharField(max_length=100)
    detection_unit_member_name = models.CharField(max_length=100)
    report_num = models.CharField(max_length=100)
    core_code_id = models.CharField(max_length=100)
    core_code_id_end = models.CharField(max_length=100)
    project_part = models.CharField(max_length=100)
    spec = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)
    exam_result = models.CharField(max_length=100)
    hnt_yhtj = models.CharField(max_length=100)
    age_time_str = models.CharField(max_length=20)
    # report_date = models.DateTimeField(blank=True)
    # detection_date = models.DateTimeField(blank=True)
    # molding_date = models.DateTimeField(blank=True)
    report_date_str = models.CharField(max_length=100)
    detection_date_str = models.CharField(max_length=100)
    molding_date_str = models.CharField(max_length=100)
    added_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('item_name', 'name')


class SampleAlert(models.Model):
    sample = models.ForeignKey(Sample)
    # Created, fixing, closed.
    status = models.CharField(max_length=10)
    create_time = models.DateTimeField()
    created_by = models.CharField(max_length=10)
    update_time = models.DateTimeField()
    updated_by = models.CharField(max_length=10)


# Camera, video and video_alert
class Camera(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    device_number = models.CharField(max_length=50)


class Video(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    #In seconds
    duration = models.IntegerField()
    # relative url
    url = models.CharField(max_length=50)


# video alert may be created by user.
class VideoAlert(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    # auto, manual
    alert_type = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    create_time = models.DateTimeField()
    created_by = models.CharField(max_length=10)
    update_time = models.DateTimeField()
    updated_by = models.CharField(max_length=10)


# Sensor, temperature_humidity data, sensor_alert
class Sensor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    device_number = models.CharField(max_length=50)
    #TODO: enum -- temperature, humidity.
    sensor_type = models.CharField(max_length=20)

class TempHumdtyData(models.Model):
    pass


class TempHumdtyAlert(models.Model):
    status = models.CharField(max_length=10)
    create_time = models.DateTimeField()
    created_by = models.CharField(max_length=10)
    update_time = models.DateTimeField()
    updated_by = models.CharField(max_length=10)


# TODO: Alert notification and subscribe.
