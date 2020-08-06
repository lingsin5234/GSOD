from rest_framework import serializers
from gsod.models import GHCND


# Weather Stations
class WeatherStations(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    elevation = serializers.FloatField()
    elevation_unit = serializers.CharField()
    us_state = serializers.CharField()


# GHCND
class GHCND_Serializer(serializers.ModelSerializer):

    class Meta:
        model = GHCND
        fields = ('station_id', 'date', 'datatype', 'attributes', 'value')
