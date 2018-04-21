# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.conf.urls import url

from ccmauth import views


urlpatterns = [
    url(r'^register$', views.RegisterView.as_view(), name='ccm_user-register'),
    url(r'^login$', views.LoginView.as_view(), name='ccm_user-login'),
    url(r'^logout$', views.LogoutView.as_view(), name='ccm_user-logout'),
    url(r'^password/change$', views.PasswordResetView.as_view(), name='ccm_user-password_change')
]


