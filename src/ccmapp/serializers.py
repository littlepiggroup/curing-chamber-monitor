# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import APIException

from ccmapp import models
from ccmapp.collect_subscribe.collect_subscribe import get_proj_ids_collected_by_user, notify_video_alert
from ccmapp.models import EzvizAccount, Project, Video, Camera, UserCollectProject

logger = logging.getLogger(__name__)


class BuildingCompanySerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=models.BuildingCompanyUser.objects.all(),
                                               required=False)
    projectlist = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Project.objects.all(), required=False)

    class Meta:
        model = models.BuildingCompany
        exclude = ('instance_id',)
        depth = 1


class BuildingCompanyUserSerializer(serializers.ModelSerializer):
    building_company = serializers.PrimaryKeyRelatedField(many=False,
                                                          queryset=models.BuildingCompany.objects.all(), required=False)

    class Meta:
        model = models.BuildingCompanyUser
        exclude = ('instance_id',)
        depth = 1


class ProjectNameSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Project.objects.all(), required=False)

    class Meta:
        model = models.ProjectName
        fields = '__all__'
        depth = 1


class ProjectSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False,
                                                          queryset=models.BuildingCompany.objects.all())
    names = ProjectNameSerializer(many=True, read_only=False)
    sensors = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Sensor.objects.all(), required=False)

    class Meta:
        model = models.Project
        exclude = ('instance_id',)
        depth = 1

    is_collect = serializers.SerializerMethodField()

    def get_is_collect(self, obj):
        collect_projs_ids = None
        if 'collect_projs_ids' in self.context.keys():
            collect_projs_ids = self.context['collect_projs_ids']
        else:
            user = self.context['request'].user
            collect_projs_ids = get_proj_ids_collected_by_user(user.pk)
            self.context['collect_projs_ids'] = collect_projs_ids
        return obj.pk in collect_projs_ids

    def create(self, validated_data):
        names_data = validated_data.pop('names')
        # project = models.Project.objects.create(**validated_data)
        project = super(ProjectSerializer, self).create(validated_data)

        for name_data in names_data:
            models.ProjectName.objects.create(project=project, **name_data)
        return project

class UserCollectProjectSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Project.objects.all(), required=True)
    user = serializers.PrimaryKeyRelatedField(many=False, queryset=models.User.objects.all(), required=True)

    class Meta:
        model = models.UserCollectProject
        depth = 1


class UserFollowProjectSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Project.objects.all(), required=True)
    user = serializers.PrimaryKeyRelatedField(many=False, queryset=models.User.objects.all(), required=True)

    class Meta:
        model = models.UserFollowProject
        depth = 1

class SampleSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(many=False, queryset=models.Project.objects.all())

    class Meta:
        model = models.Sample
        exclude = ('instance_id', 'contract')
        depth = 1

class SampleAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SampleAlert

# ----------------------------- Start: video related code -----------------------------
class EzvizAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EzvizAccount
        fields = '__all__'
        depth = 1


class CameraSerializer(serializers.ModelSerializer):
    ezviz_account = serializers.PrimaryKeyRelatedField(queryset=EzvizAccount.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = models.Camera
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        pass
        ezviz_account = validated_data['ezviz_account']
        from ccmapp.videomgr.videomgr import EzvizClient
        ezviz_client = EzvizClient(ezviz_account)
        rtmp_address = ezviz_client.get_rtmp_adr_smooth(validated_data['device_serial_number'])
        validated_data['rtmp_address'] = rtmp_address
        created_camera = models.Camera.objects.create(**validated_data)
        created_camera.save()
        return created_camera


class VideoSerializer(serializers.ModelSerializer):
    camera = serializers.PrimaryKeyRelatedField(queryset=Camera.objects.all())

    class Meta:
        model = models.Video
        fields = '__all__'
        depth = 1


class VideoAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VideoAlert

    def create(self, validated_data):
        logger.info('Create video alert')
        user= self.context['request'].user
        validated_data['created_by'] = user
        validated_data['create_time'] = timezone.now()
        validated_data['updated_by'] = user
        validated_data['update_time'] = timezone.now()
        video_alert = models.VideoAlert.objects.create(**validated_data)
        video_alert.save()
        notify_video_alert(video_alert)
        return video_alert

    def update(self, instance, validated_data):
        class AlertClosed(APIException):
            status_code = 400
            default_detail = 'Alert was already closed and can\'t be updated again.'
        if instance.status == 'CLOSED':
            raise AlertClosed()
        user = self.context['request'].user
        instance.updated_by = user
        instance.update_time = timezone.now()
        if 'description' in validated_data.keys():
            instance.description = validated_data['description']
        if 'comment' in validated_data.keys():
            instance.comment = validated_data['comment']
        if 'status' in validated_data.keys():
            instance.status = validated_data['status']
        instance.save()
        return instance

# ----------------------------- End: video related code -----------------------------
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sensor

class TemperatureAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TemperatureAlert


class HumidityAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HumidityAlert

class GlobalReportSerializer(serializers.Serializer):
    project_count = serializers.IntegerField()
    open_alert_count = serializers.IntegerField()

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Alert
        fields = '__all__'
        depth = 1
