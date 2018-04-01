# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters.rest_framework
from rest_framework import viewsets,filters
from ccm.ccmapp import models, serializers

# Create your views here.
from ccm.ccmapp.models import EzvizAccount, Camera, Video
from ccm.ccmapp.serializers import EzvizAccountSerializer, CameraSerializer, VideoSerializer


class BuildingCompanyViewSet(viewsets.ModelViewSet):
    queryset = models.BuildingCompany.objects.all()
    serializer_class = serializers.BuildingCompanySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('name', 'instance_id', 'disabled', 'added_time')
    ordering_fields = ('name', 'disabled', 'added_time')


class BuildingCompanyUserViewSet(viewsets.ModelViewSet):
    queryset = models.BuildingCompanyUser.objects.all()
    serializer_class = serializers.BuildingCompanyUserSerializer
    filter_fields = ('login_name', 'instance_id', 'disabled', 'building_company',  'added_time')
    ordering_fields = ('login_name', 'disabled', 'building_company',  'added_time')


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter,)
    filter_fields = ('status', 'nature', 'create_time', 'region', 'address',
                     'last_edit_time', 'building_company', 'instance_id', 'added_time')
    search_fields = ('nature', 'region', 'address')
    ordering_fields = ('status', 'nature', 'create_time', 'region', 'address',
                       'last_edit_time', 'building_company', 'added_time')


class ProjectNameViewSet(viewsets.ModelViewSet):
    queryset = models.ProjectName.objects.all()
    serializer_class = serializers.ProjectNameSerializer
    filter_fields = ('project', 'name', 'added_time')
    ordering_fields = ('project', 'name', 'added_time')


class ContractViewSet(viewsets.ModelViewSet):
    queryset = models.Contract.objects.all()
    serializer_class = serializers.ContractSerializer
    filter_fields = ('sign_number', 'serial_num', 'project', 'checked_date_time')
    ordering_fields = ('sign_number', 'serial_num', 'project', 'checked_date_time')


class SampleViewSet(viewsets.ModelViewSet):
    queryset = models.Sample.objects.all()
    serializer_class = serializers.SampleSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('instance_id', 'name', 'contract', 'item_id', 'item_name', 'kind_id',
                     'kind_name', 'core_code_id', 'core_code_id_end', 'status')
    search_fields = ('name',)
    ordering_fields = ('instance_id', 'name', 'contract', 'item_id', 'item_name', 'kind_id',
                       'kind_name', 'core_code_id', 'core_code_id_end', 'status')


# -------------------- Start: video related views --------------------

class EzvizAccountViewSet(viewsets.ModelViewSet):
    queryset = EzvizAccount.objects.all()
    serializer_class = EzvizAccountSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    ordering_fields = ('device_serial_number',)


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


