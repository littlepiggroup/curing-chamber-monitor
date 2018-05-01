# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime as DT
import re
from collections import OrderedDict

import django_filters.rest_framework
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.http import HttpResponse
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework import viewsets, filters, status
from rest_framework.decorators import detail_route
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from ccmapp import models, serializers
from ccmapp.collect_subscribe.collect_subscribe import get_proj_ids_collected_by_user, get_proj_ids_followed_by_user
from ccmapp.mediamgr import mediamgr

# Create your views here.
from ccmapp.mediamgr.mediamgr import remove_old_files
from ccmapp.models import EzvizAccount, Camera, Video, Project, Alert, SampleAlert, GlobalReport, VideoAlert, \
    TemperatureAlert, HumidityAlert, Sensor, UserCollectProject
from ccmapp.report.temperature_humidity import project_sensor_data_series
from ccmapp.serializers import EzvizAccountSerializer, CameraSerializer, VideoSerializer, GlobalReportSerializer, \
    SampleAlertSerializer, VideoAlertSerializer, TemperatureAlertSerializer, \
    HumidityAlertSerializer, SensorSerializer, UserCollectProjectSerializer, ProjectSerializer
from ccmapp.report import phase_report, temperature_humidity, score, project_score
import ccmapp.report.utils as report_utils
from ccmauth.serializers import UserRegisterSerializer, UserPasswordResetSerializer, UserSerializer


# ----------------------------- Start: auth related views -----------------------------

class LoginCodeAccessView(GenericAPIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        errors = None
        user_model = get_user_model()
        phone = self.request.data.get(user_model.USERNAME_FIELD)
        is_new_user = False
        if phone:
            data = {user_model.USERNAME_FIELD: phone}
            serializer = self.get_serializer(**request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if isinstance(serializer, UserRegisterSerializer):
                is_new_user = True
        else:
            errors = {'detail': _("Must include '%s'." % user_model.USERNAME_FIELD)}
        if errors:
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=(status.HTTP_201_CREATED if is_new_user else status.HTTP_200_OK))

    def get_serializer(self, **kwargs):
        user_model = get_user_model()

        try:
            user_model.objects.get(**kwargs)
            return UserPasswordResetSerializer(data=kwargs)
        except user_model.DoesNotExist:
            return UserRegisterSerializer(data=kwargs)

# ----------------------------- End: auth related views -----------------------------

def index_view(request):
    templateName = 'index.html'
    return render_to_response(templateName, RequestContext(request, locals()))

def normalize_resp(data_list):
    resp_json = [
        ("count", len(data_list)),
        ("next", None),
        ("previous", None),
        ("results", data_list)
    ]
    return OrderedDict(resp_json)

class BuildingCompanyViewSet(viewsets.ModelViewSet):
    queryset = models.BuildingCompany.objects.all()
    serializer_class = serializers.BuildingCompanySerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('id', 'name', 'disabled', 'added_time')
    ordering_fields = ('id', 'name', 'disabled', 'added_time')


class BuildingCompanyUserViewSet(viewsets.ModelViewSet):
    queryset = models.BuildingCompanyUser.objects.all()
    serializer_class = serializers.BuildingCompanyUserSerializer
    filter_fields = ('id', 'login_name', 'disabled', 'building_company', 'added_time')
    ordering_fields = ('id', 'login_name', 'disabled', 'building_company', 'added_time')


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('id', 'status', 'nature', 'create_time', 'region', 'address',
                     'last_edit_time', 'company', 'instance_id', 'added_time')
    search_fields = ('project_name',)
    ordering_fields = ('id', 'status', 'nature', 'create_time', 'region', 'address',
                       'last_edit_time', 'company', 'added_time')

    @detail_route(methods=['post'], url_path='collect')
    def collect(self, request, pk=None):
        iterator = models.UserCollectProject.objects.filter(project_id=pk, user_id=request.user.id)

        if iterator:
            # errors = {'detail': _("Project already collected.")}
            # return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_200_OK)


        try:
            project = models.Project.objects.get(id=pk)
        except models.Project.DoesNotExist:
            errors = {'detail': _("Project not existed.")}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        data = {"user": request.user.id, "project": project.id}
        serializer = serializers.UserCollectProjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['post'], url_path='uncollect')
    def uncollect(self, request, pk=None):
        iterator = models.UserCollectProject.objects.filter(project_id=pk, user_id=request.user.id)

        if iterator:
            iterator.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        # errors = {'detail': _("Project not collected.")}
        # return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['post'], url_path='follow')
    def follow(self, request, pk=None):
        iterator = models.UserFollowProject.objects.filter(project_id=pk, user_id=request.user.id)

        if iterator:
            errors = {'detail': _("Project already followed.")}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            project = models.Project.objects.get(id=pk)
        except models.Project.DoesNotExist:
            errors = {'detail': _("Project not existed.")}
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        data = {"user": request.user.id, "project": project.id}
        serializer = serializers.UserFollowProjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['post'], url_path='unfollow')
    def unfollow(self, request, pk=None):
        iterator = models.UserFollowProject.objects.filter(project_id=pk, user_id=request.user.id)

        if iterator:
            iterator.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        errors = {'detail': _("Project not followed.")}
        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectNameViewSet(viewsets.ModelViewSet):
    queryset = models.ProjectName.objects.all()
    serializer_class = serializers.ProjectNameSerializer
    filter_fields = ('id', 'project', 'name', 'added_time')
    ordering_fields = ('id', 'project', 'name', 'added_time')


class SampleViewSet(viewsets.ModelViewSet):
    queryset = models.Sample.objects.all()
    serializer_class = serializers.SampleSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('id', 'name', 'project', 'item_name', 'kind_name',
                     'core_code_id', 'core_code_id_end', 'status')
    search_fields = ('name',)
    ordering_fields = ('id', 'name', 'project', 'item_name', 'kind_name',
                       'core_code_id', 'core_code_id_end', 'status')


class SampleAlertViewSet(viewsets.ModelViewSet):
    queryset = SampleAlert.objects.all()
    serializer_class = SampleAlertSerializer

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
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('camera',)


class VideoAlertViewSet(viewsets.ModelViewSet):
    queryset = VideoAlert.objects.all()
    serializer_class = VideoAlertSerializer

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('project',)

class TemperatureHumidityReport(APIView):
    def get(self, request, format=None):
        project_id = request.GET.get('project_id')
        sensor_id = request.GET.get('sensor_id')
        time_range = request.GET.get('time_range', 'last_day')
        days = report_utils.time_para_to_days(time_range)
        return Response(normalize_resp(project_sensor_data_series(project_id, sensor_id, days)))


class TemperatureAlertViewSet(viewsets.ModelViewSet):
    queryset = TemperatureAlert.objects.all()
    serializer_class = TemperatureAlertSerializer


class HumidityAlertViewSet(viewsets.ModelViewSet):
    queryset = HumidityAlert.objects.all()
    serializer_class = HumidityAlertSerializer


class AlertViewSet(viewsets.ModelViewSet):
    queryset = models.Alert.objects.all()
    serializer_class = serializers.AlertSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)
    filter_fields = ('status', 'alert_type','project__id', 'is_open')
    search_fields = ('alert_type',)
    ordering_fields = ('alert_type',)


class GlobalReportView(APIView):
    """
    List all snippets, or create a new snippet.
    """

    # http://www.django-rest-framework.org/tutorial/3-class-based-views/
    def get(self, request, format=None):
        project_count = Project.objects.all().count()
        total_open_alerts = Alert.objects.exclude(status=SampleAlert.CLOSED).count()
        global_report = GlobalReport(project_count, total_open_alerts)
        serializer = GlobalReportSerializer(global_report)
        return Response(serializer.data)


class CompanyPhaseReportView(APIView):

    # http://www.django-rest-framework.org/tutorial/3-class-based-views/
    def get(self, request, format=None):
        company_id = request.GET.get('company_id')
        time_range = request.GET.get('time_range', 'last_week')
        days = report_utils.time_para_to_days(time_range)

        # all_projects = Project.objects.filter(company__id=company_id)
        return Response(normalize_resp(phase_report.company_phase_report(company_id, days)))


class ProjectPhaseReportView(APIView):
    def get(self, request, format=None):
        time_range = request.GET.get('time_range', 'last_week')
        company_id = request.GET.get('company_id')
        project_id = request.GET.get('project_id')
        days = report_utils.time_para_to_days(time_range)

        # end_time = DT.datetime.now()
        # start_time = end_time - DT.timedelta(days=7)
        # if time_range == 'last_month':
        #     start_time = end_time - DT.timedelta(days=30)
        #
        # groupby_project = Alert.objects.filter(create_time__lt=end_time, create_time__gt=start_time).values(
        #     'project_id').annotate(alert_count=Count('id'))
        projects_report = phase_report.company_projects_phase_report(company_id, project_id, days)
        return Response(normalize_resp(projects_report))


# Upload project image
class UploadProjectImageView(APIView):
    # parser_classes = (FileUploadParser, )
    parser_classes = (MultiPartParser,)

    # curl --verbose -X POST -S   -F "project_id=1" -F "file=@img.jpg;type=image/jpg" 127.0.0.1:8000/api/imageUpload
    def post(self, request, format=None):
        up_file = request.FILES['file']
        project_id = request.data['project_id']
        target_relative_path = 'projects/'+ project_id+ '/images'
        file_name = 'cover.jpg'
        mediamgr.create_sub_dirs(settings.MEDIA_ROOT, target_relative_path)
        target_file_path = re.sub(r'\$', '', settings.MEDIA_ROOT) + '/' + target_relative_path + '/' + file_name

        destination = open(target_file_path, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
            destination.close()

        project = Project.objects.get(pk=int(project_id))
        project.image_url = 'media/'+target_relative_path + '/' + file_name
        project.save()
        resp_data = {'project_id': project_id, 'image_url': project.image_url}
        return Response(resp_data, status.HTTP_201_CREATED)


# upload video
class UploadVideoForProject(APIView):
    parser_classes = (MultiPartParser,)

    # curl --verbose -X POST -S   -F "project_id=1" -F "file=@img.jpg;type=image/jpg" 127.0.0.1:8000/api/imageUpload
    def post(self, request, format=None):
        up_file = request.FILES['file']
        project_id = request.data['project_id']
        target_relative_path = 'projects/' + project_id + '/videos'
        datetime_now = DT.datetime.now()
        date_str = str(datetime_now.date())
        epoch_secs = int((datetime_now - DT.datetime(1970, 1, 1)).total_seconds())
        origin_file_name = up_file.name
        origin_extension = '.move' # TODO
        file_name = 'manual_video_' + date_str + "_" + str(epoch_secs) + '.mp4'
        mediamgr.create_sub_dirs(settings.MEDIA_ROOT, target_relative_path)
        target_file_path = re.sub(r'\$', '', settings.MEDIA_ROOT) + '/' + target_relative_path + '/' + file_name

        destination = open(target_file_path, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
            destination.close()

        project = Project.objects.get(pk=int(project_id))
        project.image_url = 'media/'+target_relative_path + '/' + file_name
        project.save()
        resp_data = {'project_id': project_id, 'image_url': project.image_url}
        return Response(resp_data, status.HTTP_201_CREATED)



# Generate monthly excel report

class ExcelReportView(APIView):

    def post(self, request, format='json'):
        # for now, only support months
        report_dir = 'monthly_excel_reports'
        datetime_now = DT.datetime.now()
        date_str = str(datetime_now.date())
        epoch_secs = int((datetime_now - DT.datetime(1970, 1, 1)).total_seconds())
        report_file_name = 'monthly_excel_report_' + date_str + "_" + str(epoch_secs) + '.xlsx'
        mediamgr.create_sub_dirs(settings.MEDIA_ROOT, report_dir)
        report_dir_abs_path = re.sub(r'\$', '', settings.MEDIA_ROOT) + '/' + report_dir
        file_path = report_dir_abs_path + '/' + report_file_name

        remove_old_files(report_dir_abs_path, 10)

        score.gen_final_report(file_path)
        report_url = 'media/' + report_dir + '/' + report_file_name

        resp = {'report_url': report_url}
        return Response(resp)

class CompanyScoreView(APIView):
    def get(self, request, format=None):
        time_range = request.GET.get('time_range', 'last_week')
        orderby_score_asc_para = request.GET.get('orderby_score_asc', 'true')
        orderby_score_asc = True
        if orderby_score_asc_para == 'true':
            orderby_score_asc = True
        else:
            orderby_score_asc = False

        days = report_utils.time_para_to_days(time_range)

        return Response(normalize_resp(score.gen_report_as_json(days, orderby_score_asc=orderby_score_asc)))

class ProjectScoreView(APIView):
    def get(self, request, format=None):
        company_id = request.GET.get('company_id')
        time_range = request.GET.get('time_range', 'last_week')
        orderby_score_asc_para = request.GET.get('orderby_score_asc', 'true')
        orderby_score_asc = True
        if orderby_score_asc_para == 'true':
            orderby_score_asc = True
        else:
            orderby_score_asc = False

        days = report_utils.time_para_to_days(time_range)
        user_id = request.user.id
        raw_data = project_score.company_projects_total_score(user_id,
                                        company_id, orderby_score_asc,days
                                    )

        return Response(normalize_resp(raw_data))


class ProjectCollectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self): #this method is called inside of get
        user_id = self.request.user.id
        collected_str = self.request.GET.get('is_collect', 'true')
        collected = True
        if collected_str != 'true':
            collected = False
        project_ids = get_proj_ids_collected_by_user(user_id, collected)
        queryset = self.queryset.filter(pk__in=project_ids)
        return queryset


class ProjectFollowersViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self): #this method is called inside of get
        user_id = self.request.user.id
        is_follow_str = self.request.GET.get('is_follow', 'true')
        is_follow = True
        if is_follow_str != 'true':
            is_follow = False
        project_ids = get_proj_ids_followed_by_user(user_id, is_follow)
        queryset = self.queryset.filter(pk__in=project_ids)
        return queryset

class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)