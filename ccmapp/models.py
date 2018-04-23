# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from django.db import models
from django.utils.translation import ugettext_lazy as _

# ----------------------------- Start: auth related models -----------------------------
from rest_framework.exceptions import ValidationError

from ccmauth.models import AbstractUser

_pattern = re.compile(r"^((\d{3,4}-)?\d{7,8})$|(1[3-9][0-9]{9})")


def _phone_validator(phone):
    if not _pattern.match(phone):
        raise ValidationError(
            _('%s is a invalid phone number' % phone),
        )


class User(AbstractUser):
    USERNAME_FIELD = "phone"

    phone = models.CharField(
        _('phone'),
        max_length=100,
        unique=True,
        help_text=_('Required. cell phone number.'),
        validators=[_phone_validator],
        error_messages={
            'unique': _("The phone is already registered."),
        },
    )

    class Meta:
        ordering = ('id',)

    def _generate_password(self):
        return self.phone + "_123456"

    def register_pre_process(self, validate_data):
        validate_data["password"] = self._generate_password()

    def register_post_process(self):
        print("%s\n" % self._password)

    def password_reset_pre_process(self, validate_data):
        validate_data["password"] = "old_password"
        validate_data["new_password"] = self._generate_password()

    def password_reset_post_process(self):
        print("%s\n" % self._password)

    def password_reset_password_check(self, raw_password):
        return True  # don't need to verify the password when reset new password

# ----------------------------- End: auth related models -----------------------------


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
    added_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

class City(models.Model):
    """城市"""
    name = models.CharField(max_length=64,verbose_name=u'城市名称')
    parent = models.ForeignKey('self',verbose_name=u'所属区域',null=True,blank=True)
    def project_count(self):
        return Project.objects.filter(city=self).count()
    def project_total_count(self):
        totalCount=Project.objects.filter(city=self).count()
        for eachChild in City.objects.filter(parent=self):
            totalCount += Project.objects.filter(city=eachChild).count()
        return totalCount
    
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'diary_city'
        verbose_name = '省市县'
        verbose_name_plural = '城市'

class Project(models.Model):
    PRJSTATE_TYPE_CHOICES = (
        (0,u'竣工'),
        (1,u'在建')
    )
    PRJLXSTATE_TYPE_CHOICES = (
        (0,u'未立项'),
        (1,u'已立项')
    )
    
    instance_id = models.CharField(max_length=100, unique=True, null=True)
    nature = models.CharField(max_length=20, null=True)
    num = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=256, null=True)
    status = models.IntegerField(null=True)
    create_time = models.DateTimeField(null=True)
    last_edit_time = models.DateTimeField(null=True)
    building_company = models.ForeignKey(BuildingCompany, related_name='projects',null=True)
    added_time = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(BuildingCompany,null=True,verbose_name=u'公司单位',blank=True,related_name='projectlist', on_delete=models.CASCADE)
    PrjId = models.CharField(null=True,blank=True, max_length=64,verbose_name=u'项目ID')
    PrjName = models.CharField(null=True,blank=True, max_length=128,verbose_name=u'项目名称')
    GCGS = models.CharField(null=True,blank=True,max_length=128,verbose_name=u'所属工程公司')
    GCGSID = models.CharField(null=True,blank=True,max_length=64,verbose_name=u'所属公司编号')
    PrjSFLX = models.IntegerField(verbose_name=u'是否立项',choices=PRJLXSTATE_TYPE_CHOICES, default=0)
    PrjState = models.IntegerField(null=True,blank=True,verbose_name=u'项目状态',choices=PRJSTATE_TYPE_CHOICES)
    gldw = models.CharField(null=True,blank=True,max_length=128,verbose_name=u'管理单位')
    jsdw = models.CharField(null=True,blank=True,max_length=128,verbose_name=u'建设单位')
    sjdw = models.CharField(null=True,blank=True,max_length=128,verbose_name=u'设计单位')
    kcdw = models.CharField(null=True,blank=True,max_length=128,verbose_name=u'勘察单位')
    jldw = models.CharField(null=True,blank=True,max_length=128,verbose_name=u'监理单位')
    zbdw = models.CharField(null=True,blank=True,max_length=128,verbose_name=u'总包单位')
    KGRQ = models.DateField(null=True,blank=True,verbose_name=u'开工日期')
    JGRQ = models.DateField(null=True,blank=True,verbose_name=u'竣工日期')
    XMGCS = models.CharField(null=True,blank=True,max_length=64,verbose_name=u'项目工程师')
    XMGCSID = models.CharField(null=True,blank=True,max_length=64,verbose_name=u'项目工程师ID')
    XMJL = models.CharField(null=True,blank=True,max_length=64,verbose_name=u'项目经理')
    XMJLID = models.CharField(null=True,blank=True,max_length=64,verbose_name=u'项目经理ID')
    city = models.ForeignKey('City',null=True,verbose_name=u'城市',blank=True)
    latitude = models.CharField(null=True,max_length=24,blank=True)
    longitude = models.CharField(null=True,max_length=24,blank=True)
    address = models.CharField(null=True,blank=True,max_length=128,verbose_name=u'项目地址')
    area = models.CharField(null=True,blank=True,verbose_name='面积',max_length=128,)
    price = models.CharField(null=True,blank=True,verbose_name='造价',max_length=128,)
    quality_target = models.CharField(null=True,blank=True,max_length=256,verbose_name=u'质量目标')
    safe_target = models.CharField(null=True,blank=True,max_length=256,verbose_name=u'安全目标')
    environment_target = models.CharField(blank=True,max_length=256,verbose_name=u'环境目标')
    pact_target = models.CharField(null=True,blank=True,max_length=256,verbose_name=u'合同目标')
    project_target = models.CharField(null=True,blank=True,max_length=256,verbose_name=u'项目目标')
    culture_target = models.CharField(null=True,blank=True,max_length=256,verbose_name=u'施工文明目标')
    deep = models.CharField(null=True,blank=True,verbose_name='深度',max_length=128,)
    height = models.CharField(null=True,blank=True,verbose_name='高度',max_length=128,)
    danti_nums = models.CharField(null=True,blank=True,verbose_name=u'单体数量',max_length=128)

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
    company = models.ForeignKey(BuildingCompany, on_delete=models.CASCADE,null=True)
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


class AlertType:
    SAMPLE = 0
    VIDEO = 1
    TEMPERATURE = 2
    HUMIDITY = 3


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
    sample_name = models.CharField(max_length=50,null=True)
    alert_type = models.IntegerField(null=True)
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(BuildingCompany, null=True,on_delete=models.CASCADE)
    # Created, fixing, closed.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=CREATED)
    create_time = models.DateTimeField()
    created_by = models.CharField(max_length=10)
    update_time = models.DateTimeField()
    updated_by = models.CharField(max_length=10)

    class Meta:
        ordering = ('id',)


class UserCollectProject(models.Model):
    project = models.ForeignKey(Project, related_name='+')
    user = models.ForeignKey(User, related_name='+')
    collected_time = models.DateTimeField(auto_now=True)


class UserFollowProject(models.Model):
    project = models.ForeignKey(Project, related_name='+')
    user = models.ForeignKey(User, related_name='+')
    followed_time = models.DateTimeField(auto_now=True)

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
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(BuildingCompany, null=True, on_delete=models.CASCADE)
    # auto, manual
    alert_type = models.IntegerField(null=True)
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


class TemperatureAlert(models.Model):
    alert_type = models.IntegerField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    company = models.ForeignKey(BuildingCompany, on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    create_time = models.DateTimeField()
    created_by = models.CharField(max_length=10)
    update_time = models.DateTimeField()
    updated_by = models.CharField(max_length=10)


class HumidityAlert(models.Model):
    alert_type = models.IntegerField()
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
    is_open = models.BooleanField()
    alert_type = models.IntegerField()
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
