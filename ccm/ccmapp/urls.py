# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from rest_framework import routers
from ccm.ccmapp import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'api/building_companies', views.BuildingCompanyViewSet, base_name='building_company')
router.register(r'api/building_company_users', views.BuildingCompanyUserViewSet, base_name='building_company_user')
router.register(r'api/projects', views.ProjectViewSet, base_name='project')
router.register(r'api/project_names', views.ProjectNameViewSet, base_name='project_name')
router.register(r'api/samples', views.SampleViewSet, base_name='sample')

router.register(r'api/cameras', views.CameraViewSet, base_name='camera')
router.register(r'api/ezviz_accounts', views.EzvizAccountViewSet, base_name='ezviz_account')
router.register(r'api/videos', views.VideoViewSet, base_name='video')

urlpatterns = router.urls
urlpatterns += [
    url(r'api/global_report', views.GlobalReportView.as_view()),
    url(r'api/project_phase_report', views.ProjectPhaseReportView.as_view())

]
