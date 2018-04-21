# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from rest_framework import routers

from ccmauth import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet, base_name='ccm_user')

urlpatterns = router.urls


