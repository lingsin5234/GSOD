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
    re_path(r'^usa-map/', gsod_vw.map_test),
    re_path(r'^mapbox', gsod_vw.map_box_test, name='mapbox'),
    re_path(r'^table_view/station/(?P<station_id>[:A-Z0-9]+)/$', gsod_vw.station_data_table),
    re_path(r'^contour/', gsod_vw.contour_test),
    re_path(r'^2d-test/', gsod_vw.test_2dGradient),
    re_path(r'^hexagon/', gsod_vw.hexagon_test),
    re_path(r'^test-api/', gsod_vw.test_api, name='test-api'),
    re_path(r'api/get_all_stations', gsod_vw.WeatherStationsAPI.as_view(), name='api-get-all-stations'),
    re_path(r'api/post_hexgrid', gsod_vw.HexGridAPI.as_view(), name='api-post-hexgrid'),
    re_path(r'api/get_hexgrid', gsod_vw.HexGridAPI.as_view(), name='api-get-hexgrid'),
    re_path(r'^new-map/', gsod_vw.new_map),
    re_path(r'^calculate-hexGrid/(?P<date_of_data>[\w-]+)/$', gsod_vw.calculate_hexGrid),
]
