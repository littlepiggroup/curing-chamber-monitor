# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class BuildingCompany(models.Model):
    instance_id = models.CharField(max_length=100, unique=True, null=True)
    name = models.CharField(max_length=100, unique=True)
    disabled = models.BooleanField(default=False)
    added_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)


class BuildingCompanyUser(models.Model):
    instance_id = models.CharField(max_length=100, unique=True, null=True)
    login_name = models.CharField(max_length=100, unique=True)
    building_company = models.ForeignKey(BuildingCompany, related_name='users', null=True)
    disabled = models.BooleanField(default=False)
    added_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)


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
        ordering = ('id',)


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
    item_name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, related_name='+')
    contract = models.ForeignKey(Contract, related_name='+')
    count = models.IntegerField()
    status = models.IntegerField()
    status_str = models.CharField(max_length=20)
    regular = models.BooleanField()
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
        ordering = ('id',)


class SampleAlert(models.Model):
    sample = models.ForeignKey(Sample)
    # Created, fixing, closed.
    status = models.CharField(max_length=10)
    create_time = models.DateTimeField()
    created_by = models.CharField(max_length=10)
    update_time = models.DateTimeField()
    updated_by = models.CharField(max_length=10)

    class Meta:
        ordering = ('id',)


# ----------------------------- Start: video related models -----------------------------
class EzvizAccount(models.Model):
    user_name = models.CharField(max_length=50)
    app_key = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)

    class Meta:
        ordering = ('id',)


class Camera(models.Model):
    ezviz_account = models.ForeignKey(EzvizAccount, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    device_serial_number = models.CharField(max_length=50)
    #Like: rtmp://rtmp.open.ys7.com/openlive/bfed2855f58d4dd6891e670060540a7a
    rtmp_address = models.CharField(max_length=200)

    class Meta:
        ordering = ('id',)


class Video(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    #In seconds
    save_abs_path = models.CharField(max_length=200)
    # relative url
    url_path = models.CharField(max_length=50)

    class Meta:
        ordering = ('id',)


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

    class Meta:
        ordering = ('id',)

# ----------------------------- End: video related models -----------------------------


# ----------------------------- Start: Temperature/Humidity related models -----------------------------

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

# ----------------------------- End: Temperature/Humidity related models -----------------------------


# TODO: Alert notification and subscribe (by project)
class AlertSubscriber(models.Model):
    source_project = models.ForeignKey(Project)
    # TODO: May be a phone number or wechat id? or a user id?
    subscriber = models.CharField(max_length=50)
