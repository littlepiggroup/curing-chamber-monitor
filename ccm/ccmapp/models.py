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
    project = models.ForeignKey(Project, related_name='+')
    contract = models.ForeignKey(Contract, related_name='+')
    company = models.ForeignKey(BuildingCompany, on_delete=models.CASCADE)
    instance_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    num = models.CharField(max_length=100, null=True)
    item_name = models.CharField(max_length=100)
    count = models.IntegerField(null=True)
    status = models.IntegerField(null=True)
    status_str = models.CharField(max_length=20,null=True)
    regular = models.BooleanField()
    kind_name = models.CharField(max_length=100,null=True)
    detection_unit_member_name = models.CharField(max_length=100,null=True)
    report_num = models.CharField(max_length=100, null=True)
    core_code_id = models.CharField(max_length=100,null=True)
    core_code_id_end = models.CharField(max_length=100, null=True)
    project_part = models.CharField(max_length=100, null=True)
    spec = models.CharField(max_length=100, null=True)
    grade = models.CharField(max_length=20, null=True)
    exam_result = models.IntegerField()
    hnt_yhtj = models.CharField(max_length=100,null=True)
    age_time_str = models.CharField(max_length=20,null=True)
    # report_date = models.DateTimeField(blank=True)
    # detection_date = models.DateTimeField(blank=True)
    # molding_date = models.DateTimeField(blank=True)
    report_date_str = models.CharField(max_length=100,null=True)
    detection_date_str = models.CharField(max_length=100,null=True)
    molding_date_str = models.CharField(max_length=100,null=True)
    added_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)

    def isAlert(self):
        # TODO
        mark_as_alert = False
        is_biao_zhun_yanghu = (self.hnt_yhtj == u'标准养护')
        if is_biao_zhun_yanghu:
            if not self.regular:
                mark_as_alert = True
        elif int(self.exam_result.replace('%', '')) > 100 or not self.regular:
            mark_as_alert = True
        else:
            # It is a good sample
            pass
        return mark_as_alert


class SampleAlert(models.Model):
    CREATED = 'CREATED'
    FIXING = 'FIXING'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = (
        (CREATED, 'created'),
        (FIXING, 'fixing'),
        (CLOSED, 'closed'),
    )

    sample = models.ForeignKey(Sample)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    company = models.ForeignKey(BuildingCompany, on_delete=models.CASCADE)
    # Created, fixing, closed.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=CREATED)
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
    access_token = models.CharField(max_length=200, null=True)
    access_token_expire_time = models.BigIntegerField(null=True)

    class Meta:
        ordering = ('id',)


class Camera(models.Model):
    ezviz_account = models.ForeignKey(EzvizAccount, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    device_serial_number = models.CharField(max_length=50)
    #Like: rtmp://rtmp.open.ys7.com/openlive/bfed2855f58d4dd6891e670060540a7a
    rtmp_address = models.CharField(max_length=200, null=True)

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
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    company = models.ForeignKey(BuildingCompany, on_delete=models.CASCADE)
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
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    company = models.ForeignKey(BuildingCompany, on_delete=models.CASCADE)
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

# ----------------------------- Start: Report related model -----------------------------


class GlobalReport(models.Model):
    project_amount = models.IntegerField()
    alert_amount = models.IntegerField()


class ProjectCurrentOverview(models.Model):
    NORMAL = 'NORMAL'
    ABNORMAL = 'ABNORMAL'
    STATUS_CHOICES = (
        (NORMAL, 'normal'),
        (ABNORMAL, 'abnormal')
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=NORMAL)
    project = models.ForeignKey(Project)
    sample_amount = models.IntegerField()
    camera_amount = models.IntegerField()
    sensor_amount = models.IntegerField()
    open_sample_alert_amount = models.IntegerField()
    open_video_alert_amount = models.IntegerField()
    shiqu_temperature = models.FloatField()
    shiqu_temperature_normal = models.BooleanField()
    ganqu_temperature = models.FloatField()
    ganqu_temperature_normal = models.BooleanField()
    ganqu_humidity = models.FloatField()
    ganqu_humidity_normal = models.BooleanField()

class ProjectPhaseView:
    pass
    #TODO: Maybe not a model.
    # List of time stamps
    # List of hum
    def __init__(self):
        self.names = []
        self.timestamps = []
        self.ganqu_temperature = []
        self.ganqu_humidity = []
        self.shiqu_temperature = []
        self.ganqu_humidity_alert_amount = 0
        self.ganqu_temperature_alert_amount = 0
        self.shiqu_temperature_alert_amount = 0
        self.video_alert_amount = 0
        self.sample_alert_amount = 0
        self.score = 0

# TODO: aggregate by BuildingCompany?


class BuildingCompanyReport(models.Model):
    score = models.IntegerField()

class Alert(models.Model):
    company = models.ForeignKey(BuildingCompany, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=10)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ccmapp_alert'


# ----------------------------- End: Report related model -----------------------------

class GlobalReport(object):
    def __init__(self, project_count, open_alert_count):
        self.project_count = project_count
        self.open_alert_count = open_alert_count
