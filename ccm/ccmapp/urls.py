# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import routers
from ccm.ccmapp import views

# router = routers.DefaultRouter(trailing_slash=False)
router = routers.SimpleRouter(trailing_slash=False)
router.register(r'api/building_companies', views.BuildingCompanyViewSet, base_name='building_company')
router.register(r'api/building_company_users', views.BuildingCompanyUserViewSet, base_name='building_company_user')
router.register(r'api/projects', views.ProjectViewSet, base_name='project')
router.register(r'api/project_names', views.ProjectNameViewSet, base_name='project_name')
router.register(r'api/contracts', views.ContractViewSet, base_name='contract')
router.register(r'api/samples', views.SampleViewSet, base_name='sample')

urlpatterns = router.urls
