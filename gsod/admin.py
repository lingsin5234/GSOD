from django.contrib import admin
from .models import Station, GHCND

# Register your models here.
admin.site.register(Station)
admin.site.register(GHCND)