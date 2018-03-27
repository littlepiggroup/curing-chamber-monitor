# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import routers
from ccm.ccmapp import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'api/projects', views.ProjectViewSet, base_name='project')
router.register(r'api/company', views.CompanyViewSet, base_name='company')

urlpatterns = router.urls
