"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from myfin import views
from myfin import plaid
from myfin.views import MyTokenObtainPairView, MyTokenRefreshView
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


admin.site.site_header = 'MyFin Administration'
admin.site.site_title = 'MyFin Site Admin'
admin.site.index_title = 'MyFin Site Admin Home'

router = routers.DefaultRouter()
router.register(r'myfin', views.MyFinView, 'myfin')

my_plaid = plaid.Plaid()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('csrf/', views.csrf),
    path('ping/', views.ping),
    path('api/', include(router.urls)),
    path('get_keys/', my_plaid.get_keys),
    path('api/info', my_plaid.get_info),
    path('api/create_link_token', my_plaid.create_link_token),
    path('api/set_access_token', my_plaid.get_access_token),
    path('api/transactions', my_plaid.get_transactions),
    path('authenticate_user', views.authenticate_user),
    path('user_info', views.user_info),
    path('csrf_cookie', views.GetCSRFToken.as_view()),

    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
