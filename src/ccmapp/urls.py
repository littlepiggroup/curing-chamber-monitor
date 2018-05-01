# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from rest_framework import routers
from ccmapp import views

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'api/building_companies', views.BuildingCompanyViewSet, base_name='building_company')
router.register(r'api/building_company_users', views.BuildingCompanyUserViewSet, base_name='building_company_user')
router.register(r'api/projects', views.ProjectViewSet, base_name='project')
router.register(r'api/project_collects', views.ProjectCollectViewSet, base_name='project_collect')
router.register(r'api/project_followers', views.ProjectFollowersViewSet, base_name='project_follower')
router.register(r'api/project_names', views.ProjectNameViewSet, base_name='project_name')
router.register(r'api/samples', views.SampleViewSet, base_name='sample')

router.register(r'api/ezviz_accounts', views.EzvizAccountViewSet, base_name='ezviz_account')
router.register(r'api/cameras', views.CameraViewSet, base_name='camera')
router.register(r'api/videos', views.VideoViewSet, base_name='video')
router.register(r'api/sample_alerts', views.SampleAlertViewSet, base_name='sample_alert')
router.register(r'api/video_alerts', views.VideoAlertViewSet, base_name='video_alert')

router.register(r'api/sensors', views.SensorViewSet, base_name='sensor')
router.register(r'api/temperature_alerts', views.TemperatureAlertViewSet, base_name='temperature_alert')
router.register(r'api/humidity_alerts', views.HumidityAlertViewSet, base_name='humidity_alert')

router.register(r'api/alerts', views.AlertViewSet, base_name='alert')


urlpatterns = router.urls
urlpatterns += [
    url(r'api/current_user', views.CurrentUserView.as_view()),
    url(r'api/global_report', views.GlobalReportView.as_view()),
    url(r'api/project_phase_report', views.ProjectPhaseReportView.as_view()),
    url(r'api/company_phase_report', views.CompanyPhaseReportView.as_view()),
    url(r'api/company_score_report', views.CompanyScoreView.as_view()),
    url(r'api/project_score_report', views.ProjectScoreView.as_view()),
    url(r'api/project_sensor_data_series', views.TemperatureHumidityReport.as_view()),
    url(r'api/upload_project_cover', views.UploadProjectImageView.as_view()),
    url(r'api/excel_report', views.ExcelReportView.as_view())
]
