"""ccm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url,include
from django.contrib import admin
from ccmapp import urls as rest_urls
from ccmapp import views
from ccmapp.views import index_view
from ccmauth import admin_urls as user_admin_urls
from ccmauth import urls as auth_urls
from django.conf.urls.static import  static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # auth apis including login, password reset
    url(r'^api-auth/', include(auth_urls)),
    # user crud apis - only used by administrator
    url(r'^api/', include(user_admin_urls)),
    # use phone number to get login code
    url(r'^api-auth/access_login_code$',  views.LoginCodeAccessView.as_view(), name='ccm_user-access_login_code'),
    # main apis
    url(r'^', include(rest_urls)),
    url(r'^index/', index_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

