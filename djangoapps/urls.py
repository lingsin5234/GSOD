"""noaa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path

from gsod import views as gsod_vw

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', gsod_vw.homepage),
    re_path(r'^project/', gsod_vw.project_markdown),
    re_path(r'^stations/', gsod_vw.list_stations),
    re_path(r'^edmonton-map/', gsod_vw.map_test),
    re_path(r'^mapbox', gsod_vw.map_box_test, name='mapbox'),
    re_path(r'^table_view/station/(?P<station_id>[:A-Z0-9]+)/$', gsod_vw.station_data_table)
]
